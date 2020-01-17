import configparser
from Logger import Logger
from os import path


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
            self.create_config()

    def create_config(self):
        """
        Creates a new config file
        """

        self.config['TEXTSCRIPT'] = {
            'version': self.version
        }

        self.config['HISTORY'] = {}
        self.config.set('HISTORY', '; Tracks key strokes saved history')
        self.config.set('HISTORY', 'shortcutsused', 0)
        self.config.set('HISTORY', 'shortcutchars', 0)
        self.config.set('HISTORY', 'textblockchars', 0)

        self.config['DIRECTORIES'] = {
            'defaultdirectory': 'Textblocks/',
            'localdirectory': 'None',
            'remotedirectory': 'None'
        }

        with open(self.config_dir, 'w') as configfile:
            self.config.write(configfile)

        self.log.debug(f"{self.config_dir} file created successfully.")

    def find_directories(self):
        """
        Finds the directories in the config file
        """

        self.config.read(self.config_dir)
        default_directory = self.config['DIRECTORIES']['defaultdirectory']

        return default_directory


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
