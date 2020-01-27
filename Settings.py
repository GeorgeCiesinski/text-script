import configparser
from Logger import Logger
import glib
from os import path
import datetime


class Setup:

    # TODO: Create check to ensure config file has the right categories and values

    def __init__(self, log, text_script_version):

        # Creates instance of current version variable
        self.version = text_script_version

        # TODO: Check if version has changed, update config

        # Creates instance wide log object
        self.log = log.log

        # Creates instance of ConfigParser object
        self.config = configparser.ConfigParser(allow_no_value=True)

        # Config Directory
        self.config_dir = 'Config/config.ini'

        self.log.debug("Setup initialized successfully.")

    def config_exists(self):
        """
        Checks if Config file exists
        """

        if path.exists("Config/config.ini"):

            self.log.debug("Config file found.")

        else:

            self.log.debug("No config file exists. Creating new config file.")

            # Creates new config file
            self._create_config()

    def _create_config(self):
        """
        Creates a new config file
        """

        self.config['TEXTSCRIPT'] = {}
        self.config.set('TEXTSCRIPT', '; Config file version')
        self.config.set('TEXTSCRIPT', 'version', self.version)

        self.config['HISTORY'] = {}
        self.config.set('HISTORY', '; Tracks key strokes saved history')
        self.config.set('HISTORY', 'shortcutsused', 0)
        self.config.set('HISTORY', 'shortcutchars', 0)
        self.config.set('HISTORY', 'textblockchars', 0)

        self.config['DIRECTORIES'] = {}
        self.config.set('DIRECTORIES', '; the default directory included with app, local directory, and network directory')
        self.config.set('DIRECTORIES', 'defaultdirectory', 'Textblocks/')
        self.config.set('DIRECTORIES', 'localdirectory', 'None')
        self.config.set('DIRECTORIES', 'remotedirectory', 'None')

        with open(self.config_dir, 'w') as configfile:
            self.config.write(configfile)

        self.log.debug(f"{self.config_dir} file created successfully.")

    def get_stats(self):
        """
        Gets the current usage stats from the config file.
        """

        try:

            self.config.read(self.config_dir)

            _shortcuts_used = self.config['HISTORY']['shortcutsused']
            _shortcut_chars = self.config['HISTORY']['shortcutchars']
            _textblock_chars = self.config['HISTORY']['textblockchars']

            self._print_stats(_shortcuts_used, _shortcut_chars, _textblock_chars)

        except:

            self.log.exception("Unable to get stats from config file.")
            raise

    @staticmethod
    def _print_stats(_shortcuts_used, _shortcut_chars, _textblock_chars):
        """
        Prints the usage stats to console.
        """

        _saved_keystrokes = str(int(_textblock_chars) - int(_shortcut_chars))
        _seconds_to_paste = 5
        _saved_seconds = int(_shortcuts_used) * _seconds_to_paste
        _time_saved = datetime.timedelta(seconds=_saved_seconds)

        print(f"""Your stats:

- Number of shortcuts used: {_shortcuts_used}
- You typed a total of {_shortcut_chars} shortcut characters
- Text-Script pasted a total of {_textblock_chars} characters
- You saved {_saved_keystrokes} keystrokes
- If it takes {_seconds_to_paste} seconds to copy & paste an item, you saved {_time_saved}""")

    def shortcut_setup(self, directories):
        """
        Extends shortcut_list and file_dir_list from the shortcuts and file_dirs lists.
        """

        shortcut_list = []
        file_dir_list = []

        # For each directory in directories
        for directory in directories:

            # Appends shortcuts only if directory is not None
            if directory is not None:

                # Get shortcuts and file_dirs
                shortcuts, file_dirs = self.append_directories(directory)

                # Print shortcut title
                if directory is directories[0]:
                    print("\nDefault Directory: \n")
                    self.log.debug("Appending shortcuts from default directory.")
                elif directory is directories[1]:
                    print(f"\nLocal Directory: {directory}\n")
                    self.log.debug(f"Appending shortcuts from {directory} directory.")
                elif directory is directories[2]:
                    print(f"\nRemote Directory: {directory}\n")
                    self.log.debug(f"Appending shortcuts from {directory} directory.")

                # Print shortcuts
                glib.print_shortcuts(file_dirs, shortcuts)

                # extends shortcut_list with values in shortcuts
                try:
                    shortcut_list.extend(shortcuts)
                except:
                    self.log.exception("Failed to extend shortcut_list.")
                    raise
                else:
                    self.log.debug("Successfully extended shortcut_list")

                # append file_dirs to file_dir_list
                file_dir_list.extend(file_dirs)

                self.log.debug("Successfully appended shortcuts and file_dirs.")

        return shortcut_list, file_dir_list

    def find_directories(self):
        """
        Finds the directories in the config file
        """

        self.config.read(self.config_dir)
        default_directory = self.config['DIRECTORIES']['defaultdirectory']
        local_directory = self.config['DIRECTORIES']['localdirectory']
        remote_directory = self.config['DIRECTORIES']['remotedirectory']

        if default_directory == "None" or default_directory == "":
            default_directory = None
            self.log.debug("Default directory is set to None.")
        if local_directory == "None" or local_directory == "":
            local_directory = None
            self.log.debug("Local directory is set to None.")
        if remote_directory == "None" or remote_directory == "":
            remote_directory = None
            self.log.debug("Remote directory is set to None.")

        directories = [default_directory, local_directory, remote_directory]
        self.log.debug(f"Retrieved the following directories from config: {directories}")

        return directories

    @staticmethod
    def append_directories(directory):
        """
        Creates shortcuts and file_dirs
        """

        files, file_dirs = glib.list_files(directory)

        # Creates shortcut list with the same index
        shortcuts = glib.list_shortcuts(files)

        return shortcuts, file_dirs


class UpdateConfig:

    def __init__(self, log):

        # Creates instance wide log variable
        self.log = log.log

        # Creates instance of ConfigParser
        self.config = configparser.ConfigParser(allow_no_value=True)

        # Config Directory
        self.config_dir = 'Config/config.ini'

        self.log.debug("Setup initialized successfully.")

    def update_history(self, shortcut, textblock):
        """
        Updates the shortcuts used, total shortcut characters typed, and total textblock characters pasted
        """

        # Read config file for the shortcuts used, shortcut characters, and textblock characters
        self.config.read(self.config_dir)
        shortcuts_used = int(self.config['HISTORY']['shortcutsused'])
        shortcut_chars = int(self.config['HISTORY']['shortcutchars'])
        textblock_chars = int(self.config['HISTORY']['textblockchars'])

        # Increase shortcuts used by 1
        shortcuts_used += 1

        # Increase shortcut characters by the length of the current shortcut
        shortcut_chars += len(shortcut)

        # Increase textblock characters by the length of the current textblock
        textblock_chars += len(textblock)

        # Update the config categories with the updated data
        self.config.set('HISTORY', 'shortcutsused', str(shortcuts_used))
        self.config.set('HISTORY', 'shortcutchars', str(shortcut_chars))
        self.config.set('HISTORY', 'textblockchars', str(textblock_chars))

        # Write to the config file
        with open(self.config_dir, 'w') as configfile:
            self.config.write(configfile)


if __name__ == "__main__":

    # Initialize Logger
    L = Logger()

    L.log.debug("Program started from Settings.py.")

    s = Setup(L)

    s.config_exists()
