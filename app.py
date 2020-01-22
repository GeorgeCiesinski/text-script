import glib
from Settings import Setup
from Logger import Logger
from TextController import WordCatcher, KeyboardEmulator


def shortcut_setup(directories):
    """
    Creates shortcut_list and file_dir_list
    """

    file_list, file_dir_list = glib.list_files(directories)

    # Creates shortcut list with the same index
    shortcut_list = glib.list_shortcuts(file_list)

    glib.print_shortcuts(file_dir_list, shortcut_list)

    return shortcut_list, file_dir_list


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

    # Gets a list with default, local, and remote directories
    directories = setup.find_directories()

    """
    Initialize Text Controller
    """

    shortcut_list, file_dir_list = shortcut_setup(directories)

    # Initializes KeyboardEmulator instance
    k = KeyboardEmulator(L)

    # Initialize WordCatcher
    w = WordCatcher(L, k, shortcut_list, file_dir_list)
