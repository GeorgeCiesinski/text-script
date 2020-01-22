import glib
from Settings import Setup
from Logger import Logger
from TextController import WordCatcher, KeyboardEmulator


def shortcut_setup(directories):

    shortcut_list = None
    file_dir_list = None

    # For each directory in directories
    for directory in directories:

        # Appends shortcuts only if directory is not None
        if directory is not None:

            # Get shortcuts and file_dirs
            shortcuts, file_dirs = append_directories(directory)

            # Print shortcut title
            if directory is directories[0]:
                print("Default Directory: \n")
            elif directory is directories[1]:
                print(f"Local Directory: {directory}\n")
            elif directory is directories[2]:
                print(f"Remote Directory: {directory}\n")

            # Print shortcuts


            # append shortcuts to shortcut_list
            # append file_dirs to file_dir_list




    return shortcut_list
    return file_dir_list


def append_directories(directory):
    """
    Creates shortcuts and file_dirs
    """

    files, file_dirs = glib.list_files(directories)

    # Creates shortcut list with the same index
    shortcuts = glib.list_shortcuts(files)

    glib.print_shortcuts(file_dirs, shortcuts)

    return shortcuts, file_dirs


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
