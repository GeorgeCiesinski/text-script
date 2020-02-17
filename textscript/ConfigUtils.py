import configparser
from Logger import Logger
import glib
from os import path
import datetime


class Setup:

    # TODO: Create check to ensure config file has the right categories and values

    def __init__(self, _log, text_script_version):

        # Creates instance of current version variable
        self.version = text_script_version

        # TODO: Check if version has changed, update config

        # Creates instance wide log object
        self._log = _log.log

        # Creates instance of ConfigParser object
        self._config = configparser.ConfigParser(allow_no_value=True)

        # Shortcut notification variables
        self._last_shortcuts = []
        self._new_shortcuts = []
        self._removed_shortcuts = []

        # Config Directories
        self._config_dir = "./config/"
        self._config_file_dir = "./config/config.ini"

        self._log.debug("Setup initialized successfully.")

    def check_config(self):
        """
        Checks if config file is compatible with program version. Updates old config files.
        """

        # Check if config exists, create if not
        self.config_exists()

        # Check if any sections or options are missing from the config
        self.check_config_contents()

    def config_exists(self):
        """
        Checks if Config file exists
        """

        if path.exists(self._config_file_dir):

            self._log.debug("Config file found.")

        else:

            self._log.debug("Config file not found. Creating new file.")

            # Creates new config file
            self._create_config()

    def check_config_contents(self):

        _config_sections = ['TEXTSCRIPT', 'HISTORY', 'DIRECTORIES', 'SHORTCUTS']
        _textscript_options = ['version']
        _history_options = ['shortcutsused', 'shortcutchars', 'textblockchars']
        _directories_options = ['defaultdirectory', 'localdirectory', 'remotedirectory']
        _shortcuts_options = ['lastshortcuts']

        # Read the config file
        self._config.read(self._config_file_dir)

        # Check which sections exist in config file
        _current_sections = self._config.sections()

        # If any sections are missing, add section
        for _section in _config_sections:
            if _section in _current_sections:
                self._log.info(f"The section {_section} found in config file.")
            else:
                # Todo: Consider moving into a new function
                self._log.info(f"The section {_section} is missing from config file.")
                self._config.add_section(_section)
                self._log.info(f"The section {_section} successfully added to config file.")

            # For each section, check if all options exist
            

            # If any options are missing, add option

        # Check version number
        # If Version is outdated, update version

        pass

    def _create_config(self):
        """
        Creates a new config file
        """

        # Create directory if doesn't exist
        if not glib.check_directory(self._config_dir):
            glib.create_folder(self._config_dir)
            self._log.debug("No Config directory found. Creating directory.")

        try:

            # Create config file
            self._config['TEXTSCRIPT'] = {}
            self._config.set('TEXTSCRIPT', '; Config file version')
            self._config.set('TEXTSCRIPT', 'version', self.version)

            self._config['HISTORY'] = {}
            self._config.set('HISTORY', '; Tracks key strokes saved history')
            self._config.set('HISTORY', 'shortcutsused', 0)
            self._config.set('HISTORY', 'shortcutchars', 0)
            self._config.set('HISTORY', 'textblockchars', 0)

            self._config['DIRECTORIES'] = {}
            self._config.set(
                'DIRECTORIES',
                '; the default directory included with app, local directory, and network directory'
            )
            self._config.set('DIRECTORIES', 'defaultdirectory', 'textblocks/')
            self._config.set('DIRECTORIES', 'localdirectory', 'None')
            self._config.set('DIRECTORIES', 'remotedirectory', 'None')

            self._config['SHORTCUTS'] = {}
            self._config.set('SHORTCUTS', 'lastshortcuts', "")

            with open(self._config_file_dir, 'w') as configfile:
                self._config.write(configfile)

        except configparser.Error:

            self._log.exception("Failed to create config file due to configparser error.")
            raise

        except Exception:

            self._log.exception("Failed to create config file due to unexpected error.")
            raise

        else:

            self._log.debug(f"{self._config_file_dir} file created successfully.")

    def shortcut_setup(self, _directories):
        """
        Extends _shortcut_list and _file_dir_list from the _shortcuts and _file_dirs lists.
        """

        _shortcut_list = []
        _file_dir_list = []

        # For each directory in directories
        for _directory in _directories:

            # Appends shortcuts only if directory is not None
            if _directory is not None:

                # Get shortcuts and file_dirs
                _shortcuts, _file_dirs = self._append_directories(_directory)

                # Print shortcut title
                if _directory is _directories[0]:

                    print("\nDefault Directory: \n")
                    self._log.debug("Appending shortcuts from default directory.")

                elif _directory is _directories[1]:

                    print(f"\nLocal Directory: {_directory}\n")
                    self._log.debug(f"Appending shortcuts from local directory: {_directory}")

                elif _directory is _directories[2]:

                    print(f"\nRemote Directory: {_directory}\n")
                    self._log.debug(f"Appending shortcuts from remote directory: {_directory}")

                # Print shortcuts
                self._log.info(_shortcuts)
                glib.print_shortcuts(_file_dirs, _shortcuts)

                # extends shortcut_list with values in shortcuts
                try:

                    _shortcut_list.extend(_shortcuts)

                except Exception:

                    self._log.exception("Failed to extend shortcut_list.")
                    raise

                else:

                    self._log.debug("Successfully extended shortcut_list")

                # append file_dirs to file_dir_list
                _file_dir_list.extend(_file_dirs)

                self._log.debug("Successfully appended shortcuts and file_dirs.")
                self._log.info(f"Shortcuts: {_shortcut_list}")

        return _shortcut_list, _file_dir_list

    def new_shortcut_check(self, _shortcut_list):

        # Todo: Split this into smaller functions

        self._log.info("Initializing new shortcut check.")

        # Reads the shortcuts from the shortcuts.ini file
        self._read_shortcuts()

        """
        New shortcut check
        """

        print("\nNew shortcut check: \n")

        for shortcut in _shortcut_list:

            # If shortcut isn't in the _last_shortcuts list, add it to _new_shortcuts
            if shortcut not in self._last_shortcuts:

                self._new_shortcuts.append(shortcut)

        # If there are more than zero new shortcuts, print the new shortcuts
        if len(self._new_shortcuts) == 0:

            self._log.info("No new shortcuts have been added.")
            print("No new shortcuts have been added.")

        else:

            self._log.info(f"The following shortcuts have been added:{self._new_shortcuts}")
            print("The following shortcuts have been added:")
            print(self._new_shortcuts)

        """
        Removed shortcut check
        """

        print("\nRemoved shortcut check: \n")

        for shortcut in self._last_shortcuts:

            # If shortcut is not in _shortcut_list, add it to the _removed_shortcuts list
            if shortcut not in _shortcut_list:

                self._removed_shortcuts.append(shortcut)

        # If there are more than 0 removed shortcuts, print the removed shortcuts
        if len(self._removed_shortcuts) == 1 and self._removed_shortcuts[0] == "":

            self._log.info("No shortcuts have been removed.")
            print("No shortcuts have been removed.")

        elif len(self._removed_shortcuts) > 0:

            self._log.info(f"The following shortcuts have been removed: {self._removed_shortcuts}")
            print("The following shortcuts have been removed:")
            print(self._removed_shortcuts)

        elif len(self._removed_shortcuts) == 0:

            self._log.info("No shortcuts have been removed.")
            print("No shortcuts have been removed.")

        # Replace self._last_shortcuts if list has changed
        if _shortcut_list != self._last_shortcuts:

            self._replace_last_shortcuts(_shortcut_list)

        self._log.info("Completed new shortcut check.")

    def _read_shortcuts(self):

        try:
            # Read shortcut history config file
            self._config.read(self._config_file_dir)

            self._last_shortcuts = (self._config['SHORTCUTS']['lastshortcuts']).split(', ')

        except configparser.Error:
            self._log.exception("Failed to read lastshortcuts from config file due to configparser.error.")
            raise

        except configparser.NoSectionError:

            self._log.exception("Failed to read lastshortcuts due to NoSectionError.")
            raise

        except Exception:
            self._log.exception("Failed to read lastshortcuts due to unexpected error.")
            raise

        else:
            self._log.info("Successfully read lastshortcuts from config file.")

    def _replace_last_shortcuts(self, _shortcut_list):

        _shortcut_string = ', '.join(_shortcut_list)

        try:
            self._config.set('SHORTCUTS', 'lastshortcuts', _shortcut_string)

            # Write to the config file
            with open(self._config_file_dir, 'w') as configfile:
                self._config.write(configfile)

        except configparser.Error:
            self._log.exception("Failed to update shortcut history file due to configparser Error.")
            raise

        except Exception:
            self._log.exception("Failed to update shortcut history file due to unexpected Error.")
            raise

        else:
            self._log.debug("Successfully updated shortcut history file with updated stats.")

    def get_stats(self):
        """
        Gets the current usage stats from the config file.
        """

        try:

            self._config.read(self._config_file_dir)

            _shortcuts_used = self._config['HISTORY']['shortcutsused']
            _shortcut_chars = self._config['HISTORY']['shortcutchars']
            _textblock_chars = self._config['HISTORY']['textblockchars']

        except configparser.NoSectionError:

            self._log.exception("Unable to get stats from config file: NoSectionError.")
            raise

        else:

            self._log.debug("Stats retrieved successfully.")
            self._print_stats(_shortcuts_used, _shortcut_chars, _textblock_chars)

    def _print_stats(self, _shortcuts_used, _shortcut_chars, _textblock_chars):
        """
        Prints the usage stats to console.
        """

        _saved_keystrokes = str(int(_textblock_chars) - int(_shortcut_chars))
        _seconds_to_paste = 5
        _saved_seconds = int(_shortcuts_used) * _seconds_to_paste
        _time_saved = datetime.timedelta(seconds=_saved_seconds)

        _stats = f"""Your stats:

- Number of shortcuts used: {_shortcuts_used}
- You typed a total of {_shortcut_chars} shortcut characters
- Text-Script pasted a total of {_textblock_chars} characters
- You saved {_saved_keystrokes} keystrokes
- If it takes {_seconds_to_paste} seconds to copy & paste an item, you saved {_time_saved}"""

        print(_stats)

        self._log.debug(_stats)

    def find_directories(self):
        """
        Finds the directories in the config file
        """

        self._config.read(self._config_file_dir)
        _default_directory = self._config['DIRECTORIES']['defaultdirectory']
        _local_directory = self._config['DIRECTORIES']['localdirectory']
        _remote_directory = self._config['DIRECTORIES']['remotedirectory']

        if _default_directory == "None" or _default_directory == "":
            _default_directory = None
            self._log.debug("Default directory is set to None.")
        if _local_directory == "None" or _local_directory == "":
            _local_directory = None
            self._log.debug("Local directory is set to None.")
        if _remote_directory == "None" or _remote_directory == "":
            _remote_directory = None
            self._log.debug("Remote directory is set to None.")

        _directories = [_default_directory, _local_directory, _remote_directory]
        self._log.debug(f"Retrieved the following directories from config: {_directories}")

        return _directories

    @staticmethod
    def _append_directories(_directory):
        """
        Creates shortcuts and file_dirs
        """

        _files, _file_dirs = glib.list_files(_directory)

        # Creates shortcut list with the same index
        _shortcuts = glib.list_shortcuts(_files)

        return _shortcuts, _file_dirs


class Update:

    def __init__(self, _log):

        # Creates instance wide log variable
        self._log = _log.log

        # Creates instance of ConfigParser
        self._config = configparser.ConfigParser(allow_no_value=True)

        # Config Directory
        self._config_file_dir = './config/config.ini'

        self._log.debug("Setup initialized successfully.")

    def update_history(self, shortcut, textblock):
        """
        Updates the shortcuts used, total shortcut characters typed, and total textblock characters pasted
        """

        try:

            # Read config file for the shortcuts used, shortcut characters, and textblock characters
            self._config.read(self._config_file_dir)
            shortcuts_used = int(self._config['HISTORY']['shortcutsused'])
            shortcut_chars = int(self._config['HISTORY']['shortcutchars'])
            textblock_chars = int(self._config['HISTORY']['textblockchars'])

            # Increase shortcuts used by 1
            shortcuts_used += 1

            # Increase shortcut characters by the length of the current shortcut
            shortcut_chars += len(shortcut)

            # Increase textblock characters by the length of the current textblock
            textblock_chars += len(textblock)

            # Update the config categories with the updated data
            self._config.set('HISTORY', 'shortcutsused', str(shortcuts_used))
            self._config.set('HISTORY', 'shortcutchars', str(shortcut_chars))
            self._config.set('HISTORY', 'textblockchars', str(textblock_chars))

            # Write to the config file
            with open(self._config_file_dir, 'w') as configfile:
                self._config.write(configfile)

        except configparser.Error:
            self._log.exception("Failed to update config file due to configparser Error.")
            raise
        except Exception:
            self._log.exception("Failed to update config file due to unexpected Error.")
            raise
        else:
            self._log.debug("Successfully updated config file with updated stats.")


if __name__ == "__main__":

    # Initialize Logger
    L = Logger()

    L.log.debug("Program started from ConfigUtils.py.")

    s = Setup(L)

    s.config_exists()
