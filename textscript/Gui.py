import threading
import tkinter as tk


class Gui:

    def __init__(self, _word_catcher, _log):

        # Creates instance wide log object
        self._log = _log.log
        self._log.debug("Gui: Starting Gui initialization.")

        # Creates instance wide WordCatcher object
        self._word_catcher = _word_catcher

        # Initialize root in __init__
        self._root = None

        # Threading event
        # Todo: More helpful comment
        self._stop_event = threading.Event()

        # Sets up the window layout
        self._setup_window()

        # Starts WordCatcher listener
        self._start_word_catcher()
        self._log.debug("Gui: WordCatcher started successfully.")

        # Starts the window loop
        self._log.debug("Starting root mainloop.")
        self._root.mainloop()

    def _setup_window(self):

        self._log.debug("Gui: Setting up root window.")

        # Creates the root window
        self._root = tk.Tk()

        # Sets the window corner icon
        self._root.iconbitmap(default='../assets/textscript.ico')

        # Window title
        self._root.title("Text-Script")

        # Window size
        self._root.geometry("400x400")

        self._log.debug("Root window setup successfully.")

    def _start_word_catcher(self):
        """
        Starts listener as a new thread
        """

        self._log.debug("Gui: Starting Word Catcher.")

        word_catcher_thread = self._start_thread(target=self._word_catcher.run_listener)

    def _start_thread(self, target):
        """
        Starts target as a new thread
        """

        self._log.debug("Gui: Starting new thread.")

        self._stop_event.clear()
        thread = threading.Thread(target=target)
        thread.start()
        return thread
