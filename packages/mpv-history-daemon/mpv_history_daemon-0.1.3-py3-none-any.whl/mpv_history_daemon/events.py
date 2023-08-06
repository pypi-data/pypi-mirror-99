"""
Reads the JSON event files and constructs media files
"""

import os
import re
import json
from itertools import chain
from datetime import datetime, timezone
from pathlib import Path
from typing import (
    Iterator,
    Sequence,
    List,
    NamedTuple,
    Set,
    Any,
    Dict,
    Tuple,
    Optional,
    Union,
    Callable,
)

from logzero import setup_logger  # type: ignore[import]

# TODO: better logger setup?
loglevel: str = os.environ.get("MPV_HISTORY_EVENTS_LOGLEVEL", "info").upper()
logger = setup_logger("mpv_history_events", level=loglevel)

EventType = str
EventData = Any


def parse_datetime_sec(d: Union[str, float, int]) -> datetime:
    return datetime.fromtimestamp(int(d), tz=timezone.utc)


class Media(NamedTuple):
    path: str  # local or URL path
    is_stream: bool  # if streaming from a URL
    start_time: datetime  # when the media started playing
    end_time: datetime  # when the media was closed/finished
    pause_duration: float  # how long the media was paused for (typically 0)
    media_duration: Optional[float]  # length of the media
    # title of the media (if URL, could be <title>...</title> from ytdl
    media_title: Optional[str]
    # additional metadata on what % I was through the media while pausing/playing/seeking
    actions: List[Tuple[datetime, str, float]]
    metadata: Dict[str, str]  # metadata from the file, if it exists

    @property
    def score(self) -> float:
        """Describes how much data this piece of media has, to """
        sc = 0
        if self.media_title is not None:
            sc = sc + 1
        if self.media_duration is not None:
            sc = sc + 1
        if self.pause_duration > 1.0:
            sc = sc + 1
        sc = sc + int(len(self.metadata) / 4)
        sc = sc + int(len(self.actions) / 8)
        return float(sc)

    @property
    def listen_time(self) -> float:
        return (self.end_time - self.start_time).total_seconds() - self.pause_duration


Results = Iterator[Media]


def all_history(input_files: Sequence[Path]) -> Results:
    yield from chain(*map(_read_event_stream, input_files))


# use some of the context of what this piece of media
# is to figure out if I actually watched/listened to it.
# I may have skipped a song if it only has a couple
# seconds between when it started/ended
def _actually_listened_to(m: Media) -> bool:
    listen_time: float = m.listen_time
    # if this is mpv streaming something from /dev/
    # (like my camera), ignore
    if not m.is_stream and m.path.startswith("/dev/"):
        return False
    if m.is_stream:
        # If I listened to more than 3 minutes
        return listen_time > 180
    else:
        if m.media_duration is not None and m.media_duration != 0:
            percentage_listened_to = listen_time / m.media_duration
            # if under 10 minutes (probably a song?), if I listened to at least 60%
            # if over, if I listened to at least 50%
            if m.media_duration < 600:
                return percentage_listened_to > 0.6
            else:
                # if I listened to more than 50% of the media duration or 30 minutes
                return listen_time > 1800 or percentage_listened_to > 0.5
        else:
            return listen_time > 60  # listened to more than a minute


# filter out items I probably didn't listen to
def history(
    input_files: Sequence[Path],
    filter_function: Callable[[Media], bool] = _actually_listened_to,
) -> Results:
    """
    can supply a function which accepts a 'Media' object as
    the first argument as the filter function
    """
    yield from filter(filter_function, all_history(input_files))


def _read_event_stream(p: Path) -> Results:
    # if theres a conflict, keep a 'score' by adding non-null fields on an item,
    # and return the one that has the most
    #
    # sometimes youtube-dl will show up twice ...?
    # use 'path' as a primary key to remove possible
    # duplicate event data
    items: Dict[str, Media] = {}
    for d in _reconstruct_event_stream(p):
        # required keys
        if not REQUIRED_KEYS.issubset(set(d)):
            # logger.debug("Doesnt have required keys, ignoring...")
            continue
        if d["end_time"] < d["start_time"]:
            logger.warning(f"End time is less than start time! {d}")
        m = Media(
            path=d["path"],
            is_stream=d["is_stream"],
            start_time=parse_datetime_sec(int(d["start_time"])),
            end_time=parse_datetime_sec(int(d["end_time"])),
            pause_duration=d["pause_duration"],
            media_duration=d.get("duration"),
            media_title=d.get("media_title"),
            actions=[
                (parse_datetime_sec(timestamp), data[0], data[1])
                for timestamp, data in d["actions"].items()
            ],
            metadata=d.get("metadata", {}),
        )
        # if percentage seems off, left hanging socket?? (not sure), skip
        if (
            m.is_stream is False
            and m.media_duration is not None
            and m.media_duration != 0
            and not m.path.startswith("/dev/")
        ):
            percentage_listened_to = m.listen_time / m.media_duration
            if percentage_listened_to > 5:
                logger.debug(
                    "Percentage listened to is larger than 500%, skipping {} {}".format(
                        m.path, m.start_time
                    )
                )
                continue
        key = m.path
        if key not in items:
            items[key] = m
        else:
            # use item with better score
            if m.score > items[key].score:
                logger.debug(f"replacing {items[key]} with {m}")
                items[key] = m
    yield from list(items.values())


REQUIRED_KEYS = set(["playlist_pos", "start_time", "path"])

IGNORED_EVENTS: Set[EventType] = set(
    [
        "playlist",
        "playlist-count",
    ]
)


def _destructure_event(d: Dict) -> Tuple[EventType, EventData]:
    di = d.items()
    assert len(di) == 1, "Event not in expected format!"
    return list(di)[0]


URL_REGEX = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


# https://stackoverflow.com/a/7160778/9348376
def _is_urlish(url: str) -> bool:
    return re.match(URL_REGEX, url) is not None


def _reconstruct_event_stream(p: Path) -> Iterator[Dict[str, Any]]:
    """
    Takes about a dozen events receieved chronologically from the MPV
    socket, and reconstructs what I was doing while it was playing.
    """
    events = json.loads(p.read_text())
    # mpv socket names are created like:
    #
    # declare -a mpv_options
    # mpv_options=(--input-ipc-server="${socket_dir}/$(date +%s%N)")
    # exec "$mpv_path" "${mpv_options[@]}"
    #
    # get when mpv launched from the filename
    start_time = None
    try:
        start_time = int(int(p.stem) / 1e9)
    except ValueError as ve:
        logger.warning(str(ve))

    # dictionary for storing data while we parse though events
    media_data: Dict[str, Any] = {}

    # 'globals', set at the beginning
    working_dir = os.environ["HOME"]
    is_first_item = True  # helps control how to handle duration
    # playlist_count = None
    most_recent_time: float = 0.0

    # used to help determine state
    yielded_count = 0
    is_playing = True  # assume playing at beginning
    pause_duration = 0.0  # pause duration for this entry
    pause_start_time: Optional[float] = None  # if the entry is paused, when it started
    actions: Dict[float, Tuple[str, float]] = {}

    # sort by timestamp, incase
    for dt_s in sorted(events):
        dt_float = float(dt_s)
        most_recent_time = dt_float
        event_name, event_data = _destructure_event(events[dt_s])
        if event_name in IGNORED_EVENTS:
            continue
        elif event_name == "playlist-pos":
            # reliable event to use to set start time of an item
            # the first item might have been off for 5 or so seconds
            # because of the socket_scan, so we cant use playlist-pos's
            # timestamp as the start of the mpv instance.
            # instead, we use the timestamp from the /tmp/mpvsocket/ filename
            #
            # but, if this is not the first item in the event stream,
            # use playlist-pos's timestamp as when a file starts
            if (
                "playlist_pos" in media_data
                and media_data["playlist_pos"] == event_data
            ):
                logger.debug(
                    f"Got same playlist position {event_data} twice. Current data: {media_data}"
                )
                continue
            media_data["playlist_pos"] = event_data
            if is_first_item:
                # if this is the first item, set the start time to when mpv launched
                media_data["start_time"] = start_time
                is_first_item = False  # stays false the entire function call
            else:
                media_data["start_time"] = dt_float
        elif event_name == "socket-added":
            if start_time is None:
                start_time = int(float(event_data))
        elif event_name == "working-directory":
            # shouldnt be added to media_data, affects path, but is the
            # same across the entire run of mpv
            working_dir = event_data
        elif event_name == "is-paused":
            # if this was paused when we connected to the socket,
            # assume its been paused since close to it was launched
            if event_data is True:
                is_playing = True
                pause_start_time = start_time
        elif event_name == "path":
            media_data["is_stream"] = False
            # if its ytdl://scheme
            if event_data.startswith("ytdl://"):
                media_data[event_name] = event_data.lstrip("ytdl://")
                media_data["is_stream"] = True
                continue
            if _is_urlish(event_data):
                media_data[event_name] = event_data
                media_data["is_stream"] = True
                continue
            # test if this is an absolute path
            if event_data.startswith("/"):
                media_data[event_name] = event_data
            else:
                # I think this is fine to do?
                full_path: str = os.path.join(working_dir, event_data)
                media_data[event_name] = full_path
        elif event_name == "metadata":
            # TODO: how to parse this better?
            media_data[event_name] = event_data
        elif event_name == "media-title":
            media_data["media_title"] = event_data
        elif event_name == "duration":
            # note: path is already set (if streaming, we may not get any duration)
            assert event_data is not None
            media_data[event_name] = event_data
        elif event_name in ["seek", "paused", "resumed"]:
            if event_name == "paused":
                # if a pause event was received while mpv was still playing,
                # save when it was paused, we can calculate complete pause time
                # while this piece of media was playing by combining sequences of
                # pause times
                if is_playing:
                    is_playing = False
                    pause_start_time = dt_float
                else:
                    logger.debug("received pause event while paused?")
            elif event_name == "resumed":
                # if its currently paused, and we received a resume event
                if not is_playing:
                    is_playing = True
                    # if we know when it was paused, add how long it was paused to pause_duration
                    if pause_start_time is not None:
                        pause_duration = pause_duration + (dt_float - pause_start_time)
                        pause_start_time = None
                else:
                    # logger.warning("received resumed event while already playing?")
                    pass
            if event_data is not None and "percent-pos" in event_data:
                actions[dt_float] = (event_name, event_data["percent-pos"])
        elif event_name == "eof":
            # eof is *ALWAYS* before new data gets loaded in
            # if mpv is force quit, may not have an eof.
            # check after to make sure eof/mpv-quit/final-write
            # was the last item, else write out whatever
            # media_data has in the dict currently
            if not is_playing:
                pause_duration = pause_duration + (dt_float - pause_start_time)  # type: ignore[operator]
            media_data["end_time"] = dt_float
            media_data["pause_duration"] = pause_duration
            media_data["actions"] = actions
            pause_duration = 0
            yield media_data
            yielded_count += 1
            media_data = {}
            actions = {}
        elif event_name in ["mpv-quit", "final-write"]:
            # if this happened right after an eof, it can be ignored

            # if the eof didnt happen and mpv was quit manually, save
            # quit time as end_time
            if REQUIRED_KEYS.issubset(set(media_data)):
                # if I quit while it was paused
                if not is_playing and pause_start_time is not None:
                    pause_duration = pause_duration + (dt_float - pause_start_time)
                media_data["end_time"] = dt_float
                media_data["pause_duration"] = pause_duration
                media_data["actions"] = actions
                yield media_data
                # yielded_count += 1
            return
        else:
            logger.warning(f"Unexpected event name {event_name}")

    if len(media_data) != 0:
        # if we have enough of the fields in the namedtuple, then this isnt
        # a corrupted file, its one that didnt have an eof/had events
        # after an eof for some reason
        if not REQUIRED_KEYS.issubset(set(media_data)):
            logger.debug("Ignoring leftover data... {}".format(media_data))
        else:
            # if we got through all the keys, and this has been playing for at least a minute,
            # even though this is sorta broken, log it anyways
            if most_recent_time - media_data["start_time"] > 60:
                # if it crashed while it was paused
                if not is_playing and pause_start_time is not None:
                    pause_duration = pause_duration + (
                        most_recent_time - pause_start_time
                    )
                logger.debug(
                    "slightly broken, but yielding anyways... {}".format(media_data)
                )
                media_data["end_time"] = most_recent_time
                media_data["pause_duration"] = pause_duration
                media_data["actions"] = actions
                yield media_data
