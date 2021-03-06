import glib
from Gui import Gui
from ConfigUtils import Setup
from Logger import Logger
from TextController import WordCatcher, KeyboardEmulator


def main():

    # Get's the current version from glib. Make sure this is accurate before a public release.
    text_script_version = glib.get_version()

    """
    Initialize Logger
    """

    # Initialize Logger
    L = Logger()
    L.log.debug(f"Program started from text-script. Version: {text_script_version}")

    # Output version
    print(f"Running text-script version {text_script_version}.\n")

    """
    Configure Settings
    """

    # Initialize setup
    setup = Setup(L, text_script_version)

    # Check if config file exists, and is up to date
    setup.config_exists()

    # Get stats from config
    stats = setup.get_stats()
    # Calculate remaining stats
    complete_stats = setup.calculate_stats(stats)
    # Print stats to console
    setup.print_stats(complete_stats)

    """
    Initialize Text Controller
    """

    # Gets a list with default, local, and remote directories
    directories = setup.find_directories()

    # Load shortcuts and file directories
    shortcut_list, file_dir_list = setup.shortcut_setup(directories)
    L.log.debug("text-script retrieved shortcut_list, file_dir_list:")

    # Check if new shortcuts have been added
    setup.new_shortcut_check(shortcut_list)

    # Initializes KeyboardEmulator instance
    k = KeyboardEmulator(L)

    # Initialize WordCatcher
    w = WordCatcher(L, k, shortcut_list, file_dir_list, setup)

    """
    Start Gui
    """

    # Initialize GUI
    g = Gui(w, L, setup)

    # Close program if all threads are killed
    raise SystemExit


if __name__ == "__main__":

    main()
