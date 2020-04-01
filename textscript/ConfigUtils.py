import configparser
from Logger import Logger
import glib
from os import path
import datetime


# Config file object
class Config:

    def __init__(self, version):
        """
        This init function creates three lists:
        - config_sections contains the sections and options
        - section_comments contains the comments for each section
        - config_values contains the default values for those sections
        Ensure that this is updated whenever a new section or option is needed in the config as this generates and
        repairs the existing config file.
        """

        # Key is the sections, Value is a list of options
        self.config_sections = {
            'TEXTSCRIPT': ['version'],
            'HISTORY': ['shortcutsused', 'shortcutchars', 'textblockchars'],
            'DIRECTORIES': ['defaultdirectory', 'localdirectory', 'remotedirectory'],
            'SHORTCUTS': ['lastshortcuts']  # Default is empty string
        }

        self.section_comments = {
            'TEXTSCRIPT': '; Config file version',
            'HISTORY': '; Keeps a record of the number of keystrokes, and used shortcuts',
            'DIRECTORIES': '; The default directory included with app, local directory, and network directory',
            'SHORTCUTS': '; Keeps a record of previously loaded shortcuts'  # Default is empty string
        }

        self.config_values = {
            'TEXTSCRIPT': [version],  # Default version should be current version
            'HISTORY': ['0', '0', '0'],  # Default is 0
            'DIRECTORIES': ['./textblocks/', 'None', 'None'],  # Default is none
            'SHORTCUTS': ['']  # Default is empty string
        }


class Setup:

    def __init__(self, _log, text_script_version):

        # Creates instance wide log object
        self._log = _log.log

        self._log.debug("ConfigUtils: Starting Setup initialization.")

        # Creates instance of current version variable
        self.version = text_script_version

        # Creates instance of ConfigParser object and allows empty values so comments are valid
        self._config = configparser.ConfigParser(allow_no_value=True)

        # Shortcut notification variables
        self._last_shortcuts = []
        self._new_shortcuts = []
        self._removed_shortcuts = []

        # Config Directories
        self._config_dir = "./config/"
        self._config_file_dir = "./config/config.ini"

        self._log.debug("Setup initialized successfully.")

    def config_exists(self):
        """
        Checks if Config file exists. Calls function to create a new config if doesn't exist.
        """

        self._log.debug("ConfigUtils: Starting config_exists.")

        # Create a default config
        _default_config = Config(self.version)

        if path.exists(self._config_file_dir):

            self._log.debug(f"Config file found at: {self._config_file_dir}")

            # Checks if the config is up to date or not, stores values from existing config
            self._check_config(_default_config)

        else:

            _not_found = "Config file not found. Creating new file."

            self._log.debug(_not_found)

            print(_not_found, "\n")

            # Call create config, send default config
            self._create_config(_default_config)

    def _check_config(self, _config_template):
        """
        Checks if config file is outdated. Updates or adds outdated sections & options config files.

        :param _config_template:
        """

        self._log.debug("ConfigUtils: Starting _check_config.")

        _modified_config_template = Config(self.version)  # Create a new config template to save existing config values

        _config_outdated = False  # True if any values have been modified in _modified_config_template

        _config_template_sections = _config_template.config_sections.keys()  # Get config template sections

        self._config.read(self._config_file_dir)  # Read the config file

        _current_sections = self._config.sections()  # Get config file sections

        _config_version = self._config["TEXTSCRIPT"]["version"]

        # For sections in the config template
        for _section in _config_template_sections:

            # If section is in the config file
            if _section in _current_sections:

                self._log.info(f"The section {_section} found in config file.")

                _current_options = self._config.options(_section)  # Get options for current section from config file

                # Check options. Save data from existing config
                for _option in _config_template.config_sections[_section]:

                    if _option in _current_options:

                        self._log.info(f"The option {_option} found in config file. Saving value.")

                        _current_value = self._config[_section][_option]  # Gets the value of the option

                        # Sets this value in the _modified_config_template
                        _modified_config_template.config_values[_section][_current_options.index(_option)] = _current_value

                    else:

                        self._log.info(f"The option {_option} is missing from the config file. Config is outdated.")

                        _config_outdated = True

            # If section is not in config file
            else:

                # No action required as the template contains default values

                self._log.info(f"The section {_section} is missing from config file. Config is outdated.")

                _config_outdated = True

        if _config_version != self.version:

            self._log.info(f"The config file is set to version {_config_version}. Updating to {self.version}")

            _modified_config_template.config_values["TEXTSCRIPT"][0] = self.version

            _config_outdated = True

        # If config file is outdated, update config file
        if _config_outdated is True:

            self._log.info("A section or option was missing, updating the config file.")

            self._create_config(_modified_config_template)

            self._log.info(f"Config file successfully updated to version {self.version}.")

        else:

            self._log.info(f"Config file is up to date.")

    def _create_config(self, _config_template):
        """
        Takes the dictionary values in the _config_template and creates a new config file based on this. Accepts
        either a default config or a config with modified values.

        :param _config_template:
        """

        self._log.debug("ConfigUtils: Starting _create_config.")

        # Create directory if doesn't exist
        if not glib.check_directory(self._config_dir):
            glib.create_folder(self._config_dir)
            self._log.debug("No Config directory found. Creating directory.")

        # Create a _sections list
        _sections = _config_template.config_sections.keys()

        try:

            for _section in _sections:

                # List of options for this section
                _options = _config_template.config_sections[_section]

                # Finds the section comment
                _section_comment = _config_template.section_comments[_section]

                # Creates this section
                self._config[_section] = {}

                # Writes the config comment for the section
                self._config.set(_section, _section_comment)

                for _option in _options:  # For each of the options in the list of options

                    # Find the option value at the same index
                    _option_value = _config_template.config_values[_section][_options.index(_option)]

                    # Create the option under the section and set the value
                    self._config.set(_section, _option, _option_value)

        except configparser.Error:

            self._log.exception("Failed to create config file due to configparser error.")
            raise

        except Exception:

            self._log.exception("Failed to create config file due to unexpected error.")
            raise

        else:

            self._log.debug(f"{self._config_file_dir} file created successfully.")

        # Write the config file (overwrites existing)
        with open(self._config_file_dir, 'w') as configfile:
            self._config.write(configfile)

    def shortcut_setup(self, _directories):
        """
        Extends _shortcut_list and _file_dir_list from the _shortcuts and _file_dirs lists.
        """

        self._log.debug("ConfigUtils: Starting shortcut_setup.")

        # Todo: Check if exception handling is required here.

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

                # extend file_dirs to file_dir_list
                _file_dir_list.extend(_file_dirs)

                self._log.debug("Successfully appended shortcuts and file_dirs.")
                self._log.info(f"Shortcuts: {_shortcut_list}")

        return _shortcut_list, _file_dir_list

    def new_shortcut_check(self, _shortcut_list):
        """
        Checks if any shortcuts have been added or removed since the last time program was run.

        :param _shortcut_list:
        """

        self._log.debug("ConfigUtils: Starting new_shortcut_check.")

        # Todo: Split this into smaller functions

        self._log.info("Reading lastshortcuts.")
        self._read_shortcuts

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

        self._log.debug("Completed new shortcut check.")

    def _read_shortcuts(self):
        """
        Reads the lastshortcuts option from config file to determine the shortcuts last loaded by program.
        """

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
        """
        Updates lastshortcuts with currently loaded shortcuts

        :param _shortcut_list:
        """

        _shortcut_string = ', '.join(_shortcut_list)

        try:
            self._config.set('SHORTCUTS', 'lastshortcuts', _shortcut_string)

            # Write to the config file
            with open(self._config_file_dir, 'w') as configfile:
                self._config.write(configfile)

        except configparser.Error:
            self._log.exception("Failed to update lastshortcuts due to configparser Error.")
            raise

        except configparser.NoSectionError:

            self._log.exception("Failed to update lastshortcuts due to NoSectionError.")
            raise

        except Exception:
            self._log.exception("Failed to update lastshortcuts due to unexpected Error.")
            raise

        else:
            self._log.debug("Successfully updated lastshortcuts with updated stats.")

    def get_stats(self):
        """
        Gets the current usage stats from the config file.
        """

        self._log.debug("ConfigUtils: Starting get_stats.")

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
            self._calculate_stats(_shortcuts_used, _shortcut_chars, _textblock_chars)

    def _calculate_stats(self, _shortcuts_used, _shortcut_chars, _textblock_chars):
        """
        Prints the usage stats to console.
        """

        self._log.debug("ConfigUtils: Starting _calculate_stats.")

        try:

            _saved_keystrokes = str(int(_textblock_chars) - int(_shortcut_chars))
            _seconds_to_paste = 5
            _saved_seconds = int(_shortcuts_used) * _seconds_to_paste
            _time_saved = datetime.timedelta(seconds=_saved_seconds)

        except ValueError:

            self._log.exception("The config file contains invalid values in the HISTORY section.")

            _value_error_message = """Stats failed to calculate due to a value error. Your stats have been reset to 0 
to correct the error."""

            print(_value_error_message, "\n")

            # Repairs history
            self._repair_history()

        else:

            self._log.info("The stats were calculated successfully.")

            _stats = f"""Your stats:

- Number of shortcuts used: {_shortcuts_used}
- You typed a total of {_shortcut_chars} shortcut characters
- Text-Script pasted a total of {_textblock_chars} characters
- You saved {_saved_keystrokes} keystrokes
- If it takes {_seconds_to_paste} seconds to copy & paste an item, you saved {_time_saved}"""

            print(_stats)

            self._log.info(_stats)

    def _repair_history(self):
        """
        Repairs history section if an invalid value is found there.
        """

        self._log.debug("ConfigUtils: Starting _repair_history.")

        try:

            # Open the config file
            self._config.read(self._config_file_dir)

            # Reset HISTORY values to 0
            self._config.set('HISTORY', 'shortcutsused', "0")
            self._config.set('HISTORY', 'shortcutchars', "0")
            self._config.set('HISTORY', 'textblockchars', "0")

        except configparser.Error:
            self._log.exception("Failed to read shortcut history due to configparser Error.")
            raise

        except configparser.NoSectionError:

            self._log.exception("Failed to read shortcut history due to NoSectionError.")
            raise

        except Exception:
            self._log.exception("Failed to read shortcut history due to unexpected Error.")
            raise

        else:
            self._log.debug("Successfully read shortcut history.")

        try:

            # Write to the config file
            with open(self._config_file_dir, 'w') as configfile:
                self._config.write(configfile)
                self._log.debug("Successfully repaired HISTORY.")

        except OSError:

            self._log.exception("Failed to repair history due to OSError.")

        else:

            # Run get_stats again after repair
            self.get_stats()

    def find_directories(self):
        """
        Finds the directories in the config file
        """

        self._log.debug("ConfigUtils: Starting find_directories.")

        try:

            self._config.read(self._config_file_dir)

        except configparser.Error:

            self._log.exception("Failed to read directories due to configparser Error.")
            raise

        except configparser.NoSectionError:

            self._log.exception("Failed to read directories due to NoSectionError.")
            raise

        except Exception:

            self._log.exception("Failed to read directories due to unexpected Error.")
            raise

        else:

            # Assign the default, local, and remote directory with value from config file
            _default_directory = self._config['DIRECTORIES']['defaultdirectory']
            _local_directory = self._config['DIRECTORIES']['localdirectory']
            _remote_directory = self._config['DIRECTORIES']['remotedirectory']

            if _default_directory == "None" or _default_directory == "":
                _default_directory = None
                self._log.debug("Default directory is set to None.")
            else:
                self._log.debug(f"Default directory is set to {_default_directory}")

            if _local_directory == "None" or _local_directory == "":
                _local_directory = None
                self._log.debug("Local directory is set to None.")
            else:
                self._log.debug(f"Local directory is set to {_local_directory}")

            if _remote_directory == "None" or _remote_directory == "":
                _remote_directory = None
                self._log.debug("Remote directory is set to None.")
            else:
                self._log.debug(f"Remote directory is set to {_remote_directory}")

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

    def save_settings(self, _directories):
        """
        Overwrites the directories in config.ini
        """

        try:
            self._log.debug("ConfigUtils: Attempting to save new directories.")

            # Read config file for the shortcuts used, shortcut characters, and textblock characters
            self._config.read(self._config_file_dir)

            # Update the config categories with the updated data
            self._config.set('DIRECTORIES', 'defaultdirectory', _directories[0])
            self._config.set('DIRECTORIES', 'localdirectory', _directories[1])
            self._config.set('DIRECTORIES', 'remotedirectory', _directories[2])

            # Write to the config file
            with open(self._config_file_dir, 'w') as configfile:
                self._config.write(configfile)

        except configparser.Error:
            self._log.exception("Failed to update config file due to configparser Error.")
            raise

        except OSError:
            self._log.exception("Failed to update config file due to OSError.")
            raise

        except Exception:
            self._log.exception("Failed to update config file due to unexpected Error.")
            raise

        else:
            self._log.debug("Successfully updated config file with updated stats.")
            return True

class Update:

    def __init__(self, _log):

        # Creates instance wide log variable
        self._log = _log.log

        # Creates instance of ConfigParser
        self._config = configparser.ConfigParser(allow_no_value=True)

        # Config Directory
        self._config_file_dir = './config/config.ini'

        self._log.debug("Update initialized successfully.")

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

        except OSError:
            self._log.exception("Failed to update config file due to OSError.")
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
