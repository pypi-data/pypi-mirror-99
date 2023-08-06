import curses
import glob
import importlib
import threading
from typing import List
import subprocess
from os.path import dirname, basename, isfile

import castero
from castero import helpers
from castero.config import Config
from castero.database import Database
from castero.downloadqueue import DownloadQueue
from castero.feed import Feed, FeedError, FeedLoadError, FeedDownloadError, \
    FeedParseError, FeedStructureError
from castero.episode import Episode
from castero.menu import Menu
from castero.perspective import Perspective
from castero.queue import Queue
from castero.player import Player


class DisplayError(Exception):
    """An ambiguous error while handling the display.
    """


class DisplaySizeError(DisplayError):
    """The display does not have acceptable dimensions.
    """


class Display:
    """The user-facing display.

    This class is used to handle all user-interaction. It creates and handles
    all aspects of the application's interface, including windows and menus. It
    retrieves input from the user and performs corresponding actions.
    """
    MIN_WIDTH = 20
    MIN_HEIGHT = 8
    INPUT_TIMEOUT = int(Config["refresh_delay"])
    UPDATE_TIMEOUT = 2000 / INPUT_TIMEOUT  # multiple of INPUT_TIMEOUT
    STATUS_TIMEOUT = 3  # multiple of UPDATE_TIMEOUT
    COLOR_NAMES = {
        'black': curses.COLOR_BLACK,
        'blue': curses.COLOR_BLUE,
        'cyan': curses.COLOR_CYAN,
        'green': curses.COLOR_GREEN,
        'magenta': curses.COLOR_MAGENTA,
        'red': curses.COLOR_RED,
        'white': curses.COLOR_WHITE,
        'yellow': curses.COLOR_YELLOW,
        'transparent': -1
    }
    KEY_MAPPING = {chr(i): i for i in range(256)}
    KEY_MAPPING.update(
        (name[4:], value) for name, value in vars(curses).items()
        if name.startswith('KEY_')
    )
    KEY_MAPPING.update(
        {
            'ENTER': 10,
            'SPACE': 32
        }
    )
    AVAILABLE_PLAYERS = {}

    def __init__(self, stdscr, database) -> None:
        """
        Args:
            stdscr: a stdscr from curses.initscr()
            database: a connected castero.Database
        """
        self._stdscr = stdscr
        self._database = database
        self._parent_x = -1
        self._parent_y = -1
        self._perspectives = {}
        self._active_perspective = 1
        self._header_window = None
        self._footer_window = None
        self._queue = Queue(self)
        self._download_queue = DownloadQueue(self)
        self._status = ""
        self._header_str = ""
        self._footer_str = ""
        self._status_timer = self.STATUS_TIMEOUT
        self._update_timer = self.UPDATE_TIMEOUT
        self._menus_valid = True
        self._modified_episodes = []

        # basic preliminary operations
        self._stdscr.timeout(self.INPUT_TIMEOUT)
        curses.start_color()
        curses.use_default_colors()
        curses.noecho()
        self._curs_set(0)
        curses.cbreak()
        self._stdscr.keypad(True)

        self.update_parent_dimensions()
        self.create_color_pairs()
        self._load_perspectives()
        self._load_players()
        self._restore_queue()
        self._create_windows()
        self.create_menus()

    def color_number(self, color: str) -> int:
        """Convert color string to valid color number"""
        if color in self.COLOR_NAMES:
            return self.COLOR_NAMES[color]
        if color.isnumeric() and int(color) < curses.COLORS:
            return int(color)
        return -1

    def create_color_pairs(self) -> None:
        """Initializes color pairs used for the display.

        Creates the following color pairs (foreground, background):
            - 1: foreground, background
            - 2: background, foreground
            - 3: background_alt, foreground_alt
            - 4: foreground_alt, background_alt
            - 5: foreground_dim, background
        """

        curses.init_pair(
            1,
            self.color_number(Config["color_foreground"]),
            self.color_number(Config["color_background"]),
        )
        curses.init_pair(
            2,
            self.color_number(Config["color_background"]),
            self.color_number(Config["color_foreground"]),
        )
        curses.init_pair(
            3,
            self.color_number(Config["color_background_alt"]),
            self.color_number(Config["color_foreground_alt"]),
        )
        curses.init_pair(
            4,
            self.color_number(Config["color_foreground_alt"]),
            self.color_number(Config["color_background_alt"]),
        )
        curses.init_pair(
            5,
            self.color_number(Config["color_foreground_dim"]),
            self.color_number(Config["color_background"]),
        )
        curses.init_pair(
            6,
            self.color_number(Config["color_foreground_status"]),
            self.color_number(Config["color_background"]),
        )
        curses.init_pair(
            7,
            self.color_number(Config["color_foreground_heading"]),
            self.color_number(Config["color_background"]),
        )
        curses.init_pair(
            8,
            self.color_number(Config["color_foreground_dividers"]),
            self.color_number(Config["color_background"]),
        )

    def _load_perspectives(self) -> None:
        """Load instances of perspectives from the `perspectives` package.
        """
        # load a list of modules names by manually detecting .py files
        module_files = glob.glob(dirname(__file__) + "/perspectives/*.py")
        module_names = [basename(f)[:-3] for f in module_files if isfile(f)]

        for name in module_names:
            p_mod = importlib.import_module("castero.perspectives.%s" % name)
            p_cls = getattr(
                p_mod,
                dir(p_mod)[[cls.lower() == name
                            for cls in dir(p_mod)].index(True)])
            inst = p_cls(self)
            self._perspectives[inst.ID] = inst

    def _load_players(self) -> None:
        """Load player classes from the `players` package.
        """
        # load a list of modules names by manually detecting .py files
        module_files = glob.glob(dirname(__file__) + "/players/*.py")
        module_names = [basename(f)[:-3] for f in module_files if isfile(f)]

        for name in module_names:
            p_mod = importlib.import_module("castero.players.%s" % name)
            p_cls = getattr(
                p_mod,
                dir(p_mod)[[cls.lower() == name
                            for cls in dir(p_mod)].index(True)])
            self.AVAILABLE_PLAYERS[p_cls.NAME] = p_cls

    def _restore_queue(self) -> None:
        """Recreate players in queue from the database.
        """
        for episode in self.database.queue():
            player = Player.create_instance(
                self.AVAILABLE_PLAYERS, str(episode),
                episode.get_playable(), episode)
            self.queue.add(player)

    def _create_windows(self) -> None:
        """Creates and sets basic parameters for the windows.

        If the windows already exist when this method is run, this method will
        delete them and create new ones.
        """
        # delete old windows if they exist
        if self._header_window is not None:
            del self._header_window
            self._header_window = None
        if self._footer_window is not None:
            del self._footer_window
            self._footer_window = None

        # create windows
        self._header_window = curses.newwin(2, self._parent_x,
                                            0, 0)
        self._footer_window = curses.newwin(2, self._parent_x,
                                            self._parent_y - 2, 0)

        # create windows for all perspectives
        for perspective_id in self._perspectives:
            self._perspectives[perspective_id].create_windows()

    def create_menus(self) -> None:
        """Creates the menus used in each window.

        Windows which have menus should be created prior to running this method
        (using _create_windows).
        """
        for perspective_id in self._perspectives:
            self._perspectives[perspective_id].create_menus()

    def show_help(self) -> None:
        """Show the help screen.

        This method takes over the main loop, displaying the screen until a key
        is pressed. This means that typical loop actions, including checking
        the state of the current player, will not run while this screen is up.
        """
        help_lines = castero.__help__.split('\n')

        # the first and last lines that content can be displayed, excluding
        # the final line on the screen which is reserved for the "press any
        # key to exit" line
        y_bounds = (0, self._parent_y - 2)

        # the current vertical offset set by the user with arrow keys
        cur_offset = 0

        # the max offset, which is the offset where the last line in help_lines
        # is displayed at y_bounds[1]
        max_offset = len(help_lines) - (y_bounds[1] - y_bounds[0]) - 2

        help_window = curses.newwin(self._parent_y, self._parent_x, 0, 0)
        help_window.refresh()

        running = True
        update_text = True
        while running:
            inp = self._stdscr.getch()

            if inp == self.KEY_MAPPING["DOWN"]:
                update_text = True
                cur_offset += 1

            elif inp == self.KEY_MAPPING["UP"]:
                update_text = True
                cur_offset -= 1
            elif inp != -1:
                running = False

            if cur_offset > max_offset:
                cur_offset = max_offset
            if cur_offset < 0:
                cur_offset = 0

            if update_text:
                # draw blank lines to clear the screen
                for i in range(self._parent_y):
                    help_window.addstr(i, 0, "".ljust(self._parent_x - 1))

                # add text from help_lines based on offset
                max_lineno = min(len(help_lines), cur_offset + y_bounds[1] + 1)
                for i in range(cur_offset, max_lineno):
                    help_window.addstr(
                        i - cur_offset, 2, help_lines[i][:self._parent_x - 2])

                bottom_line = "[%d/%d] Press arrow keys to scroll, or any"\
                    " other key to exit this screen." % (
                        min(len(help_lines), cur_offset + y_bounds[1] + 2),
                        len(help_lines)
                    )
                help_window.addstr(y_bounds[1] + 1, 2, bottom_line)
                help_window.refresh()
                update_text = False

        self.clear()
        self.display_all()

    def display(self) -> None:
        """Draws all windows and sub-features, including titles and borders.
        """
        # check if the screen size has changed
        self.update_parent_dimensions()

        # decrement the update timer
        self._update_timer -= 1
        if self._update_timer <= 0:
            self._update_timer = self.UPDATE_TIMEOUT
            self.update()

        # display the header and footer
        width = self._header_window.getmaxyx()[1]
        self._header_window.addstr(0, 0, " " * width)
        self._header_window.addstr(0, 0, self._header_str,
                                   curses.color_pair(6) | curses.A_BOLD)
        self._footer_window.addstr(1, 0, self._footer_str[:width - 1],
                                   curses.color_pair(6) | curses.A_BOLD)

        # add window borders
        self._header_window.hline(1, 0,
                                  0, self._header_window.getmaxyx()[1],
                                  curses.ACS_HLINE | curses.color_pair(8))
        self._footer_window.hline(0, 0,
                                  0, self._footer_window.getmaxyx()[1],
                                  curses.ACS_HLINE | curses.color_pair(8))

        # refresh updated windows
        self._footer_window.refresh()
        self._header_window.refresh()

        # add display for current perspective
        self._perspectives[self._active_perspective].display()

    def display_all(self) -> None:
        """Force all perspectives to completely redraw their content.

        For more details, see the description of the method in Perspective.
        """
        self.refresh()
        self._perspectives[self._active_perspective].display_all()
        self.refresh()

    def _get_active_perspective(self) -> Perspective:
        """Retrieve the active/visible Perspective.
        """
        return self._perspectives[self._active_perspective]

    def _change_active_perspective(self, perspective_id) -> None:
        """Changes _active_perspective to the given perspective.

        Args:
            perspective_id: the ID of the perspective to change to
        """
        assert perspective_id in self._perspectives

        self.clear()
        self._active_perspective = perspective_id
        self._perspectives[perspective_id].made_active()
        self.display_all()

    def _get_input_str(self, prompt) -> str:
        """Prompts the user for input and returns the resulting string.

        This method assumes that all input strings will be obtained in the
        footer window.

        Args:
            prompt: a string to inform the user of what they need to enter

        Returns:
            str: the user's input
        """
        assert self._footer_window is not None
        assert isinstance(prompt, str)

        self._curs_set(1)
        self._stdscr.timeout(-1)  # disable timeouts while waiting for entry

        # display input prompt
        self._footer_window.addstr(
            1, 0, " " * (self._footer_window.getmaxyx()[1] - 1)
        )
        self._footer_window.addstr(1, 0, prompt)

        entry_pad = curses.newpad(1, 999)
        current_x = 0
        scroll_x = 0
        input_char = None
        while input_char not in [curses.KEY_ENTER, 10]:
            if input_char is not None:
                # manually handle backspace
                if input_char in [curses.KEY_BACKSPACE, 127]:
                    if current_x > 0:
                        entry_pad.delch(0, current_x - 1)
                        current_x -= 1
                        if scroll_x > 0:
                            scroll_x -= 1
                else:
                    # scroll the input pad if necessary
                    if current_x + len(prompt) > \
                            self._footer_window.getmaxyx()[1] - 1:
                        scroll_x += 1

                    # add the entered character to the pad
                    entry_pad.addch(0, current_x, input_char)
                    current_x += 1

                # display current portion of pad
                entry_pad.refresh(0, scroll_x,
                                  self._parent_y - 1, len(prompt),
                                  self._parent_y - 1,
                                  self._footer_window.getmaxyx()[1] - 1)

            # get the next input character
            input_char = self._footer_window.getch()

        self._stdscr.timeout(self.INPUT_TIMEOUT)
        self._footer_window.clear()
        self._curs_set(0)

        return entry_pad.instr(0, 0, entry_pad.getmaxyx()[1]) \
            .decode('utf-8').strip()

    def _get_y_n(self, prompt) -> bool:
        """Prompts the user for a yes or no (y/n) input.

        Args:
            prompt: a string to inform the user of what they need to enter

        Returns:
            bool: true if the user presses y, false otherwise
        """
        assert self._footer_window is not None
        assert isinstance(prompt, str)

        curses.echo()
        self._curs_set(1)

        self._footer_window.addstr(
            1, 0, " " * (self._footer_window.getmaxyx()[1] - 1)
        )
        self._footer_window.addstr(1, 0, prompt)
        char = self._footer_window.getch()

        self._footer_window.clear()
        self._curs_set(0)
        curses.noecho()

        return char == ord('y')

    def _curs_set(self, visibility: int) -> None:
        """Safely set the appearance of the cursor.

        Args:
            visibility: 0 (invisible), 1 (normal mode) or 2 (high visibility)
        """
        if hasattr(curses, 'curs_set'):
            try:
                curses.curs_set(visibility)
            except curses.error:
                pass

    def handle_input(self, c) -> bool:
        """Performs action corresponding to the user's input.

        Args:
            c: the input character

        Returns:
            bool: whether or not the application should continue running
        """
        for perspective_id in self._perspectives:
            if c == self.KEY_MAPPING[str(perspective_id)]:
                self._change_active_perspective(perspective_id)

        return self._get_active_perspective().handle_input(c)

    def add_feed(self) -> None:
        """Prompt the user for a feed and add it, if possible.
        """
        path = self._get_input_str("Enter the URL or path of the feed: ")
        try:
            # assume urls have http in them
            if "http" in path:
                feed = Feed(url=path)
            else:
                feed = Feed(file=path)
            if feed.validated:
                self.database.replace_feed(feed)
                self.database.replace_episodes(feed, feed.parse_episodes())
            self.menus_valid = False
            self.change_status("Feed '%s\' successfully added" % str(feed))
        except FeedError as e:
            if isinstance(e, FeedLoadError):
                self.change_status(
                    "FeedLoadError: %s" % str(e)
                )
            elif isinstance(e, FeedDownloadError):
                self.change_status(
                    "FeedDownloadError: %s" % str(e)
                )
            elif isinstance(e, FeedParseError):
                self.change_status(
                    "FeedParseError: %s" % str(e)
                )
            elif isinstance(e, FeedStructureError):
                self.change_status(
                    "FeedStructureError: %s" % str(e)
                )
            else:
                self.change_status(
                    "FeedError [ambiguous]: %s" % str(e)
                )

    def delete_feed(self, feed: Feed) -> None:
        """Deletes the given feed from the database.

        If the delete_feed_confirmation config option is true, this method will
        first ask for y/n confirmation before deleting the feed.

        Deleting a feed also deletes all downloaded/saved episodes.

        Args:
            feed: the Feed to delete, which can be None
        """
        if feed is not None:
            should_delete = True
            if helpers.is_true(Config["delete_feed_confirmation"]):
                should_delete = self._get_y_n(
                    "Are you sure you want to delete this feed? (y/n): "
                )
            if should_delete:
                self.database.delete_feed(feed)
                self.menus_valid = False
                self.change_status("Feed successfully deleted")

    def reload_feeds(self) -> None:
        """Reloads the users' feeds.

        If the total number of feeds is >= the reload_feeds_threshold config
        option, this method will first ask for y/n confirmation.

        This method starts the reloading in a new un-managed thread.
        """
        should_reload = True
        if len(self.database.feeds()) >= int(Config["reload_feeds_threshold"]):
            should_reload = self._get_y_n(
                "Are you sure you want to reload all of your feeds?"
                " (y/n): "
            )
        if should_reload:
            t = threading.Thread(target=self.database.reload, args=[self])
            t.start()

    def reload_selected_feed(self, feed: Feed) -> None:
        """Reloads the selected feed.

        This method starts the reloading in a new un-managed thread.
        """
        t = threading.Thread(target=self.database.reload, args=[self, [feed]])
        t.start()

    def save_episodes(self, feed=None, episode=None) -> None:
        """Save a feed or episode.

        Exactly one of either feed or episode must be given.

        Args:
            feed: (optional) a feed to download all episodes of
            episode: (optional) an episode to download
        """
        assert (feed is None or episode is None) and (feed is not episode)

        if feed is not None:
            num_to_save = 0
            for episode in self.database.episodes(feed):
                if not episode.downloaded:
                    num_to_save += 1

            if num_to_save == 0:
                return

            should_delete = self._get_y_n(
                    "Are you sure you want to download %d"
                    " episodes from this feed? (y/n): " % num_to_save)
            if should_delete:
                for episode in self.database.episodes(feed):
                    if not episode.downloaded:
                        self._download_queue.add(episode)
        else:
            if not episode.downloaded:
                self._download_queue.add(episode)

    def delete_episodes(self, feed=None, episode=None) -> None:
        """Delete a downloaded episode, or all of those from a feed.

        Exactly one of either feed or episode must be given.

        Args:
            feed: (optional) a feed to delete all episodes of
            episode: (optional) an episode or delete
        """
        assert (feed is None or episode is None) and (feed is not episode)

        if feed is not None:
            num_deleted = 0
            num_to_delete = 0
            for episode in self.database.episodes(feed):
                if episode.downloaded:
                    num_to_delete += 1

            if num_to_delete == 0:
                return

            should_delete = self._get_y_n(
                    "Are you sure you want to delete %d downloaded"
                    " episodes from this feed? (y/n): " % num_to_delete)
            if should_delete:
                for episode in self.database.episodes(feed):
                    if episode.downloaded:
                        episode.delete(self)
                        num_deleted += 1
                self.menus_valid = False
                self.change_status(
                    "Successfully deleted %d episodes" % num_deleted)
        else:
            if episode.downloaded:
                should_delete = self._get_y_n(
                    "Are you sure you want to delete the downloaded"
                    " episode? (y/n): ")
                if should_delete:
                    episode.delete(self)

    def filter_menu(self, menu: Menu) -> None:
        menu.filter_text = self._get_input_str("Filter: ")
        self.menus_valid = False

    def execute_command(self, episode: Episode) -> None:
        """Execute a system command on an episode's enclosure.

        The command to run is set by the user with the execute_command config
        setting. See the description in the config file above that setting for
        details about how it may be formatted.

        Args:
            episode: episode to execute the command on
        """
        command = Config["execute_command"]\
            .replace("{file}", episode.enclosure)\
            .replace("{title}", episode.title)\
            .replace("{description}", episode.description)\
            .replace("{link}", episode.link)\
            .replace("{pubdate}", episode.pubdate)\
            .replace("{copyright}", episode.copyright)
        subprocess.Popen(command, shell=True)

    def show_episode_url(self, episode: Episode) -> None:
        """Show episode URL in status line.

        Args:
            episode: episode to show URL for
        """
        if episode is not None:
            max_width = self._footer_window.getmaxyx()[1] - 1
            self._footer_window.addstr(
                1, 0, " " * max_width
            )
            self.change_status(episode.enclosure)

    def clear(self) -> None:
        """Clear the screen.
        """
        self._stdscr.clear()

    def refresh(self) -> None:
        """Refresh the screen and all windows in all perspectives.
        """
        self._stdscr.refresh()

        for perspective_id in self._perspectives:
            self._perspectives[perspective_id].refresh()

        self._header_window.refresh()
        self._footer_window.refresh()

    def terminate(self) -> None:
        """Set console settings to their normal state.

        This method does not, by itself, cause the application to exit. Nor
        does it even cause the input loop to end. It should simply be seen as
        a "wrapping up" method for any actions which need to be performed
        before the object is destroyed.
        """
        self._queue.stop()

        self.database.replace_queue(self._queue)
        self.database.close()

        curses.nocbreak()
        self._stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def update_parent_dimensions(self) -> None:
        """Update _parent_x and _parent_y to the size of the console.
        """
        current_y, current_x = self._stdscr.getmaxyx()

        if current_y != self._parent_y or current_x != self._parent_x:
            self._parent_y, self._parent_x = current_y, current_x
            self._create_windows()
            self.menus_valid = False
            self._update_timer = 0

        if self._parent_y < self.MIN_HEIGHT:
            raise DisplaySizeError("Display height is too small")
        if self._parent_x < self.MIN_WIDTH:
            raise DisplaySizeError("Display width is too small")

    def getch(self) -> int:
        """Gets an input character from the user.

        This method returns after at most INPUT_TIMEOUT ms.

        Returns:
            int: the character entered by the user, or -1
        """
        char = self._stdscr.getch()
        return char

    def change_status(self, status) -> None:
        """Changes the status message displayed in the footer.

        Args:
            status: the status message to display
        """
        assert isinstance(status, str)

        self._status = status
        self._status_timer = self.STATUS_TIMEOUT

    def update(self) -> None:
        """Updates all actively tracked components of this object.

        Should be called by the main loop after every input or input timeout.
        """
        # have the queue check if it needs to go to the next player
        self._queue.update()

        # check the status of any downloads
        try:
            self._download_queue.update()
        except OSError as e:
            self.change_status("OSError: %s" % str(e))
            return

        # check to see if menu contents have been invalidated
        if not self.menus_valid:
            for perspective_id in self._perspectives:
                self._perspectives[perspective_id].update_menus()
            self.menus_valid = True

        # update the header text
        max_width = self._header_window.getmaxyx()[1]
        header_str = "%s " % castero.__title__
        stats_str = "[%d%%]" % self._queue.volume
        if self._queue.first is not None:
            state = self._queue.first.state
            header_str += ["Stopped", "Playing", "Paused"][state] + \
                ": %s" % self._queue.first.title
            if self._queue.length > 1:
                header_str += " (+%d in queue)" % (self._queue.length - 1)

            # the stats section of the header contains the volume and, if
            # something is playing, time/duration of the media
            stats_str += " [%s]" % self._queue.first.time_str

        # truncate the header string to ensure there is always space for
        # the stats to be displayed
        header_str = header_str[:max_width - len(stats_str)]
        header_str += stats_str.rjust(max_width - len(header_str))
        self._header_str = header_str[:max_width]

        # update the footer text
        footer_str = "%sPress %s for help" % (
            self._status + " -- " if len(self._status) > 0 else "",
            Config["key_help"])
        max_width = self._footer_window.getmaxyx()[1] - 1
        footer_str = footer_str[:max_width]
        self._footer_str = footer_str.ljust(max_width)[:max_width]

        # decrement the status timer
        if self._status_timer > 0:
            self._status_timer -= 1
            if self._status_timer <= 0:
                # status_timer should be reset during the next change_status()
                self._status = ""

        # write any episode modifications to the database
        if len(self._modified_episodes) > 0:
            for episode in self._modified_episodes:
                self.database.replace_episode(episode._feed, episode)
                if episode.progress is None:
                    self.database.delete_progress(episode, episode.progress)
                else:
                    self.database.replace_progress(episode, episode.progress)

            self.menus_valid = False
            self._modified_episodes = []

    @property
    def parent_x(self) -> int:
        """int: the width of the parent screen, in characters"""
        return self._parent_x

    @property
    def parent_y(self) -> int:
        """int: the height of the parent screen, in characters"""
        return self._parent_y

    @property
    def database(self) -> Database:
        """Database: the user's database"""
        return self._database

    @property
    def perspectives(self) -> dict:
        """dict: the loaded Perspective's with id:perspective pairs"""
        return self._perspectives

    @property
    def queue(self) -> Queue:
        """Queue: the Queue of Player's"""
        return self._queue

    @property
    def menus_valid(self) -> bool:
        """bool: whether the menu contents are valid (!need_to_be_updated)"""
        return self._menus_valid

    @menus_valid.setter
    def menus_valid(self, menus_valid) -> None:
        self._menus_valid = menus_valid

    @property
    def modified_episodes(self) -> List[Episode]:
        """List[Episode]: database episodes to save on the next update"""
        return self._modified_episodes
