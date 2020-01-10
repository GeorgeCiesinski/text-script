import glib
from Logger import Logger
from Gui import Gui
from TextController import WordCatcher, KeyboardEmulator


def start_text_controller(logger):

    # Gets file_list and file_dir_list
    textblock_dir = "Textblocks/"

    file_list, file_dir_list = glib.list_files(textblock_dir)

    # Creates shortcut list with the same index
    shortcut_list = glib.list_shortcuts(file_list)

    # Initializes KeyboardEmulator instance
    k = KeyboardEmulator(logger)

    # Initialize WordCatcher
    w = WordCatcher(logger, k, shortcut_list, file_dir_list)


def start_gui(logger):

    # Main instance logger
    log = logger.log

    # Create GUI object
    g = Gui(logger)

    # Close program if window is destroyed
    g.root.protocol("WM_DELETE_WINDOW", g.on_closing)

    # Tkinter main loop
    log.debug("Starting Tkinter mainloop.")
    g.root.mainloop()


if __name__ == "__main__":

    # Initialize Logger
    L = Logger()

    L.log.debug("Program started from App.py.")

    # Initializes process to start
    start_text_controller(L)

    start_gui(L)
