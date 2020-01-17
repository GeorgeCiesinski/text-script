import glib
from Settings import Setup
from Logger import Logger
from TextController import WordCatcher, KeyboardEmulator


if __name__ == "__main__":

    # Current app version / / Ensure this is correct during updates
    text_script_version = "1.1.0"

    """
    Initialize Logger
    """

    # Initialize Logger
    L = Logger()

    L.log.debug(f"Program started from App.py. Version: {text_script_version}")

    """
    Configure Settings
    """

    # Initialize setup
    setup = Setup(L, text_script_version)

    # Check if config file exists
    setup.config_exists()

    # Gets file_list and file_dir_list
    textblock_dir = setup.find_directories()

    """
    Initialize Text Controller
    """

    file_list, file_dir_list = glib.list_files(textblock_dir)

    # Creates shortcut list with the same index
    shortcut_list = glib.list_shortcuts(file_list)

    glib.print_shortcuts(file_dir_list, shortcut_list)

    # Initializes KeyboardEmulator instance
    k = KeyboardEmulator(L)

    # Initialize WordCatcher
    w = WordCatcher(L, k, shortcut_list, file_dir_list)
