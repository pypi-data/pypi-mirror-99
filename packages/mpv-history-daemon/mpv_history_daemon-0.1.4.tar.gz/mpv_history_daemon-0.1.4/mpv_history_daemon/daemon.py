"""
This probably isn't optmized/the minimum amount of code to do this
Dealing with sockets/EOFs/random drops is a pain, so this stays on the safe side
of validating to make sure sockets arent left dangling or data isn't
saved, because of a ConnectionRefusedError/BrokenPipe/general OSErrors

logzero logs all the exceptions, incase theyre not what I expect
most of the times, mpv will be open for more than 10 minutes, so
the WRITE_PERIOD periodically writes will at least capture what was
being listened to, even if *somehow* (is not common case)
I lose data on what happened
when mpv EOFd/disconnected due to a BrokenPipe.
BrokenPipes are captured in the event_eof function
"""

import os
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from time import sleep, time

from python_mpv_jsonipc import MPV  # type: ignore[import]
from logzero import logger, logfile  # type: ignore[import]


KNOWN_EVENTS = set(
    [
        "socket-added",  # custom event, for when the socket was added
        "mpv-quit",
        "playlist-count",
        "is-paused",
        "eof",
        "seek",
        "paused",
        "resumed",
        "metadata",
        "duration",
        "playlist-pos",
        "media-title",
        "path",
        "working-directory",
        "final-write",  # custom event, for when the dead/dangling socket was removed, and file was written
    ]
)

# every 10 minutes
WRITE_PERIOD = 600


def new_event(event_name: str, event_data: Any = None) -> Dict[str, Any]:
    """
    helper to create an event. validates the event name
    """
    if event_name not in KNOWN_EVENTS:
        logger.warning(f"Unknown event: {event_name}")
    return {event_name: event_data}


# disabled for now
def clean_playlist(mpv_playlist_response: List[Dict]) -> List[str]:
    """
    simplifies the playlist response from mpv
    from:
        {'filename': '01 Donuts (Outro).mp3'}, {'filename': '02 Workinonit.mp3', 'current': True, 'playing': True},...
    to:
        ['01 Donuts (Outro).mp3', ...]
    """
    filenames: List[str] = []
    for pinfo in mpv_playlist_response:
        if "filename" not in pinfo:
            logger.warning(f"No filename in playlist info!: {pinfo}")
        else:
            filenames.append(pinfo["filename"])
    # truncate to 50 filenames
    return filenames[:50]


class SocketData:
    """
    Stores Metadata for a socket with timestamps in memory
    Writes out to the JSON file when the MPV process ends

    Want to save:
        # at mpv launch:
            # playlist
            # playlist-count
            # working-directory
            # is-paused
        # event-based
            # whenever a socket is played/paused
            # whenever a file changes (eof-reached) save metadata about whats being played
                # metadata
                # media-title
                # path
                # playlist-pos
                # duration
    """

    # TODO: create signal handler to write out on keyboardinterrupt?
    def __init__(self, socket: MPV, socket_loc: str, data_dir: str):
        self.socket = socket
        self.socket_loc = socket_loc
        self.data_dir = data_dir
        self.socket_time = socket_loc.split("/")[-1]
        self.events: Dict[float, Dict] = {}
        # write every 10 minutes, even if mpv doesnt exit
        self.write_at = time() + WRITE_PERIOD
        # keep track of playlist/playlist-count, so we can use eof to determine
        # whether we should read next metadata
        self.playlist_count = self.socket.playlist_count
        playlist_pos = self.socket.playlist_pos
        # incremented at the top of in store_file_metadata
        # technically this is zero-indexed, but have to deal with off-by-one errors
        # because I cant read the playlist position of a dead socket, counting manually
        if playlist_pos is None:
            logger.warning(
                "Couldn't get playlist position in SocketData initialization, defaulting to 0"
            )
            self.playlist_index = 0
        else:
            self.playlist_index = playlist_pos
        self.store_initial_metadata()
        self.store_file_metadata()

    @property
    def event_count(self):
        return len(self.events)

    _repr_attrs = ("socket", "socket_loc", "event_count")

    def __repr__(self) -> str:
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                [
                    "=".join([a, str(getattr(self, a))])
                    for a in self.__class__._repr_attrs
                ]
            ),
        )

    __str__ = __repr__

    def write(self):
        with open(
            os.path.join(self.data_dir, f"{self.socket_time}.json"), "w"
        ) as event_f:
            json.dump(self.events, event_f)

    def nevent(self, event_name: str, event_data: Optional[Any] = None) -> None:
        """add an event"""
        ct = time()
        logger.debug(f"{self.socket_time}|{ct}|{event_name}|{event_data}")
        self.events[ct] = new_event(event_name, event_data)

    def store_initial_metadata(self):
        self.nevent("socket-added", time())
        self.nevent("working-directory", self.socket.working_directory)
        self.nevent("playlist-count", self.socket.playlist_count)
        self.nevent("is-paused", self.socket.pause)
        # self.nevent("playlist", clean_playlist(self.socket.playlist))

    def poll_for_property(
        self, attr: str, event_name: str, tries: int = 20, create_event: bool = True
    ) -> Any:
        """
        Some properties arent set when the file starts?
        sleeps for 0.1 of a second between tries (20 * 0.1 = 2 seconds)

        if create_event, once it has a non-None value, it sets the value
        with self.nevent
        """
        for _ in range(tries):
            value = getattr(self.socket, attr)
            if value is not None:
                if create_event:
                    self.nevent(event_name, value)
                return value
            sleep(0.1)
        else:
            logger.warning(f"{self.socket_loc} Couldn't poll for {event_name}")

    def store_file_metadata(self):
        """
        Called when EOF is reached (so, another file starts)
        """

        self.playlist_index += 1
        # (is zero indexed, but incrementing before making any requests out to the socket)
        if self.playlist_index - 1 >= self.playlist_count:
            logger.debug("Reached end of playlist, not reading in next file info...")
            return

        # poll for these incase theyre not set for some reason, because
        # the file was just loaded by mpv
        actual_playlist_pos = self.poll_for_property("playlist_pos", "playlist-pos")
        # make sure internal, manually counted playlist index is accurate
        if actual_playlist_pos is not None:
            if actual_playlist_pos + 1 != self.playlist_index:
                self.playlist_index = actual_playlist_pos + 1
        self.poll_for_property("path", "path")
        self.poll_for_property("media_title", "media-title")

        # weird, metadata and duration arent received at the beginning of the file?
        # poll for duration and metadata
        # maybe these have to be parsed and there done a bit after the file is read
        self.poll_for_property("metadata", "metadata")
        self.poll_for_property("duration", "duration")

    def event_resumed(self) -> None:
        """
        Called when the media is resumed, also save % in file
        """
        self.nevent("resumed", {"percent-pos": self.socket.percent_pos})

    def event_paused(self) -> None:
        """
        Called when the media is paused, also save % in file
        """
        self.nevent("paused", {"percent-pos": self.socket.percent_pos})

    def event_eof(self):
        """
        Called when the 'eof' event happens. Doesn't necessarily mean mpv exits
        Could be going to the next song in the current playlist
        (This doesnt happen the first time a song is loaded)

        Though, this is also called when mpv exits, so we should wrap the
        possible socket errors
        """
        self.nevent("eof")
        try:
            self.store_file_metadata()  # store info about new file thats playing
        # possible errors thrown: BrokenPipeError, OSError
        except Exception as e:
            logger.warning(f"Ignoring error: {e}")
            if not isinstance(e, ConnectionRefusedError):
                logger.exception(e)

    def event_seeking(self):
        """
        Called when the user seeks in the file. Could possibly be called when a file is loaded as well
        """
        if self.socket.percent_pos < 2:
            # logger.debug("ignoring seek because we just EOFd?")
            pass
        else:
            # save what % we seeked to
            self.nevent("seek", {"percent-pos": self.socket.percent_pos})


class LoopHandler:
    """
    Handles keeping track of currently live mpv instances, attaching handlers,
    the main loop.
    """

    def __init__(self, socket_dir: str, data_dir: str):
        self.data_dir: str = data_dir
        self.socket_dir: str = socket_dir
        self._socket_dir_path: Path = Path(socket_dir).expanduser().absolute()
        self.sockets: Dict[str, MPV] = {}
        self.socket_data: Dict[str, SocketData] = {}
        self.run_loop()

    def scan_sockets(self):
        """
        Look for any new sockets at socket_dir, remove any dead ones
        """
        socket_loc: str = None
        try:
            # iterate through all files
            for socket_name in os.listdir(self.socket_dir):
                socket_loc: str = os.path.join(self.socket_dir, socket_name)
                if socket_loc not in self.sockets:
                    # each of these runs in a separate thread, so the while loop below doesnt block event data
                    # ConnectionRefusedError thrown here
                    new_sock = MPV(
                        start_mpv=False,
                        ipc_socket=socket_loc,
                        quit_callback=lambda: self.remove_socket(socket_loc),
                    )
                    self.sockets[socket_loc] = new_sock
                    # if the socket gets disconnected for some reason, and we're recreating MPV, *never* overwrite data
                    if socket_loc in self.socket_data:
                        self.socket_data[socket_loc].socket = new_sock
                    else:
                        self.socket_data[socket_loc] = SocketData(
                            new_sock, socket_loc, self.data_dir
                        )
                    self.attach_observers(socket_loc, new_sock)
                    self.debug_internals()
                else:  # if this socket is already connected, just try to get the path from the scoket
                    # may have been a TimeoutError: No response from MPV.
                    # which resulted in the socket remaning in self.sockets, even if its eof'd and exited
                    self.sockets[socket_loc].path
            # iterate through sockets, if file doesnt exist for some reason
            # this is probably unnecessary
            for s_loc, sock_obj in self.sockets.items():
                # update higher scope to allow usage in except block
                socket_loc = s_loc
                # try to access path to possibly cause ConnectionRefusedError,
                # removing a dead socket
                sock_obj.path
        except (ConnectionRefusedError, BrokenPipeError):
            logger.debug(
                f"Connected refused for socket at {socket_loc}, removing dead/dangling socket file..."
            )
            # make sure its actually removed from active sockets
            # gets removed from socket_data after 10 seconds
            if socket_loc in self.sockets:
                self.remove_socket(socket_loc)
            # rm -f
            try:
                os.remove(socket_loc)
            except FileNotFoundError:
                pass

    def attach_observers(self, socket_loc: str, sock: MPV) -> None:
        """
        Watch for user pausing, eof-file (file ending)
        """
        # sanity-check
        if hasattr(sock, "_watching_instance"):
            logger.warning("Tried to attach observers twice!")
            return
        setattr(sock, "_watching_instance", None)

        socket_data: SocketData = self.socket_data[socket_loc]

        # keep track of when last EOF was. EOF also happens when
        # a file is loaded, and seeking happens when you load a file,
        # (since its sort of seeking to the beginning)
        # doesnt seem to be deterministic/easy to filter seeks out
        # by EOFs, and might match actual seeking. so, will have
        # to do larger analysis on the dumped data to figure out
        # if EOF next to seek, remove the seek

        @sock.property_observer("pause")
        def on_pause(_name, value):
            if value:  # item is now paused
                socket_data.event_paused()
            else:
                socket_data.event_resumed()

        @sock.property_observer("eof-reached")
        def on_eof(_name, value):
            # value == False means that eof has not been reached
            if isinstance(value, bool) and not value:
                return
            if value is not None:
                logger.warning(
                    "Seems that this is supposed to be None; just to signify event? not sure why it isnt"
                )
            socket_data.event_eof()

        @sock.property_observer("seeking")
        def on_seek(_name, value):
            if isinstance(value, bool) and value:
                socket_data.event_seeking()

    def remove_socket(self, socket_loc: str) -> None:
        if socket_loc in self.sockets:
            logger.debug(f"Removing socket {socket_loc}")
            del self.sockets[socket_loc]
            # write quit event
            self.socket_data[socket_loc].nevent("mpv-quit", time())
        else:
            logger.warning(
                "called remove socket, but socket_loc doesnt exist in self.sockets"
            )
        # (doesnt remove the file here, but should find it on the next scan_sockets call and remove it then)

    def debug_internals(self):
        logger.debug("sockets {}".format(self.sockets))
        logger.debug("socket_data {}".format(self.socket_data))

    def periodic_write(self):
        now = time()
        for socket_loc, socket_data in self.socket_data.items():
            if now > socket_data.write_at:
                logger.debug(f"{socket_data.socket_time}|running periodic write")
                socket_data.write()
                socket_data.write_at = now + WRITE_PERIOD
                self.debug_internals()

    def write_data(self):
        """
        Write out any completed SocketData to disk
        """
        # if the /tmp/mpvsockets/ file is no longer in self.sockets
        # but we have socketdata for it from when it was alive, in
        # self.socket_data, write that out to data_dir
        #
        # runs in the main thread, errors crash main thread
        for socket_loc in list(self.socket_data):
            if socket_loc not in self.sockets:
                logger.info(f"{socket_loc}: writing to file...")
                self.socket_data[socket_loc].nevent("final-write", time())
                self.socket_data[socket_loc].write()
                del self.socket_data[socket_loc]
                self.debug_internals()

    def run_loop(self):
        logger.debug("Starting mpv-history-daemon loop...")
        while True:
            self.scan_sockets()
            self.periodic_write()
            self.write_data()
            sleep(10)
            # TODO: watch for new files instead?


def run(socket_dir: str, data_dir: str, log_file: str) -> None:
    # if the daemon launched before any mpv instances
    if not os.path.exists(socket_dir):
        os.makedirs(socket_dir)
    assert os.path.isdir(socket_dir)
    os.makedirs(data_dir, exist_ok=True)
    assert os.path.isdir(data_dir)
    logfile(log_file, maxBytes=1e7, backupCount=1)
    # TODO: wrap LoopHandler in an infinite loop, notify-send fatal errors?
    LoopHandler(socket_dir, data_dir)
