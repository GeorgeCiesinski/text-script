import configparser
from Logger import Logger
from os import path


class Setup:

    def __init__(self, log):

        # Creates instance wide log variable
        self.log = log.log

        # Creates instance of ConfigParser
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

    def update_history(self, shortcut, textblock):

        self.config.read(self.config_dir)
        shortcuts_used = int(self.config['HISTORY']['shortcutsused'])
        shortcut_chars = int(self.config['HISTORY']['shortcutchars'])
        textblock_chars = int(self.config['HISTORY']['textblockchars'])

        shortcuts_used += 1
        shortcut_chars += len(shortcut)
        textblock_chars += len(textblock)

        self.config.set('HISTORY', 'shortcutsused', shortcuts_used)
        self.config.set('HISTORY', 'shortcutchars', shortcut_chars)
        self.config.set('HISTORY', 'textblockchars', textblock_chars)

        with open(self.config_dir, 'wb') as configfile:
            self.config.write(configfile)


if __name__ == "__main__":

    # Initialize Logger
    L = Logger()

    L.log.debug("Program started from Settings.py.")

    s = Setup(L)

    s.config_exists()
