import threading
import tkinter as tk


class Gui:

    def __init__(self, w):

        # Creates instance wide WordCatcher object
        self.w = w

        # Initialize root in __init__
        self.root = None

        # Threading event
        # Todo: More helpful comment
        self.stop_event = threading.Event()

        # Sets up the window layout
        self.setup_window()

        # Starts the window loop
        self.root.mainloop()

    def setup_window(self):

        # Creates the root window
        self.root = tk.Tk()

        # Sets the window corner icon
        self.root.iconbitmap(default='../assets/textscript.ico')

        # Window title
        self.root.title("Text-Script")

        # Window size
        self.root.geometry("400x400")

        # Starts WordCatcher listener
        self.start_word_catcher()

    def start_word_catcher(self):
        """
        Starts listener as a new thread
        """

        word_catcher_thread = self.start_thread(target=self.w.run_listener)

    def start_thread(self, target):
        """
        Starts target as a new thread
        """

        self.stop_event.clear()
        thread = threading.Thread(target=target)
        thread.start()
        return thread
