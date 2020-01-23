import glib
from Settings import Setup
from Logger import Logger
from TextController import WordCatcher, KeyboardEmulator


def shortcut_setup(log, directories):

    log = log.log

    shortcut_list = []
    file_dir_list = []

    # For each directory in directories
    for directory in directories:

        # Appends shortcuts only if directory is not None
        if directory is not None:

            # Get shortcuts and file_dirs
            shortcuts, file_dirs = append_directories(directory)

            # Print shortcut title
            if directory is directories[0]:
                print("\nDefault Directory: \n")
                log.debug("Appending shortcuts from default directory.")
            elif directory is directories[1]:
                print(f"\nLocal Directory: {directory}\n")
                log.debug(f"Appending shortcuts from {directory} directory.")
            elif directory is directories[2]:
                print(f"\nRemote Directory: {directory}\n")
                log.debug(f"Appending shortcuts from {directory} directory.")

            # Print shortcuts
            glib.print_shortcuts(file_dirs, shortcuts)

            # extends shortcut_list with values in shortcuts
            try:
                shortcut_list.extend(shortcuts)
            except:
                log.exception("Failed to extend shortcut_list.")
                raise
            else:
                log.debug("Successfully extended shortcut_list")

            # append file_dirs to file_dir_list
            file_dir_list.extend(file_dirs)

            log.debug("Successfully appended shortcuts and file_dirs.")

        elif directory is None:

            # Update Log
            if directory is directories[0]:
                log.debug("Default directory set to None.")
            elif directory is directories[1]:
                log.debug("Local directory set to None.")
            elif directory is directories[2]:
                log.debug("Remote directory set to None.")

    return shortcut_list, file_dir_list


def append_directories(directory):
    """
    Creates shortcuts and file_dirs
    """

    files, file_dirs = glib.list_files(directory)

    # Creates shortcut list with the same index
    shortcuts = glib.list_shortcuts(files)

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

    shortcut_list, file_dir_list = shortcut_setup(L, directories)

    # Initializes KeyboardEmulator instance
    k = KeyboardEmulator(L)

    # Initialize WordCatcher
    w = WordCatcher(L, k, shortcut_list, file_dir_list)
