import glib
import threading
import tkinter as tk
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

    # Print stats to console
    setup.get_stats()

    # Gets a list with default, local, and remote directories
    directories = setup.find_directories()

    """
    Initialize Text Controller
    """

    # Load shortcuts and file directories
    shortcut_list, file_dir_list = setup.shortcut_setup(directories)

    # Todo: Check if this log is required.
    L.log.debug("text-script retrieved shortcut_list, file_dir_list:")

    # Check if new shortcuts have been added
    setup.new_shortcut_check(shortcut_list)

    # Initializes KeyboardEmulator instance
    k = KeyboardEmulator(L)

    # Initialize WordCatcher
    w = WordCatcher(L, k, shortcut_list, file_dir_list, setup)

    """
    Setup GUI
    """

    root = tk.Tk()

    root.title("Text-Script")

    root.geometry("400x400")

    start_word_catcher(w)

    root.mainloop()


def start_thread(target):

    stop_event.clear()
    thread = threading.Thread(target=target)
    thread.start()
    return thread


def start_word_catcher(w):

    word_catcher_thread = start_thread(target=w.run_listener)


if __name__ == "__main__":

    stop_event = threading.Event()

    main()
