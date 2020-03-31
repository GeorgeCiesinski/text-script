import glib
import threading
import webbrowser
import tkinter as tk


class Gui:

    def __init__(self, _word_catcher, _log):

        # Creates instance wide log object
        self._log = _log.log
        self._log.debug("Gui: Starting Gui initialization.")

        # Imports WordCatcher object initialized in text-script
        self._word_catcher = _word_catcher

        # Sends the self object to TextController so the Tkinter window can be closed
        self._word_catcher.set_gui(self)

        # Initialize root in __init__
        self._root = None

        # Threading event: used for communication between threads
        self._stop_event = threading.Event()

        # Sets up the window layout
        self._setup_window()

        # Starts WordCatcher listener
        self._start_word_catcher()
        self._log.debug("Gui: WordCatcher started successfully.")

        # Close program if window is destroyed
        self._root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Starts the window loop
        self._log.debug("Starting root mainloop.")
        self._root.mainloop()

    def _setup_window(self):
        """
        Window Setup
        """

        self._log.debug("Gui: Setting up root window.")

        # Creates the root window
        self._root = tk.Tk()

        # Sets the window corner icon
        self._root.iconbitmap(default='../assets/textscript.ico')

        # Window title
        self._root.title("Text-Script")

        # Window size
        self._root.geometry("400x400")

        # Create menu
        self._create_menu()

        self._log.debug("Root window setup successfully.")

    def _create_menu(self):

        # Create menu object
        _menu = tk.Menu(self._root)
        self._root.config(menu=_menu)
        self._log.debug("Gui: Successfully created top menu.")

        # File menu
        _file_menu = tk.Menu(_menu, tearoff=False)
        _menu.add_cascade(label="File", underline=0, menu=_file_menu)

        # File Menu
        _file_menu.add_command(
            label="Settings",
            command=self._open_settings
        )
        _file_menu.add_command(
            label="Quit",
            underline=0,
            command=self.close_text_script,
            accelerator="Ctrl+Q"
        )

        # Help Menu
        _help_menu = tk.Menu(_menu, tearoff=False)
        _menu.add_cascade(label="Help", underline=0, menu=_help_menu)

        # Help Menu
        _help_menu.add_command(
            label="How to Use",
            command=self._open_help
        )
        _help_menu.add_command(
            label="Documentation",
            command=self._open_documentation
        )

        # Shortcuts for menu options
        self._root.bind_all("<Control-q>", self.close_text_script)
        self._root.bind_all("<Control-h>", self._do_nothing())

    def _open_settings(self):
        """
        Opens a window with the available settings. Alters the config file.
        """

        # Creates a new window
        self._settings_window = tk.Tk()

        # Window Setup
        self._settings_window.title("Settings")
        self._settings_window.iconbitmap(default='../assets/textscript.ico')  # Sets the window corner icon

    def _open_help(self):
        """
        Opens a window with the Text-Script Instructions
        """

        # Help text
        _help_text = glib.help_text()

        # Creates a new window
        self._help_window = tk.Tk()

        # Window Setup
        self._help_window.title("How to use Text-Script")
        self._help_window.iconbitmap(default='../assets/textscript.ico')  # Sets the window corner icon

        # Labels
        _help_label = tk.Label(
            self._help_window,
            justify="left",
            text=_help_text,
        )

        # Packs labels into window
        _help_label.grid(row=0, column=0, sticky="w", padx=4, pady=2)

    def _open_documentation(self):
        """
        Shows the user the link to the documentation and offers to open this in browser. Selecting no closes the window.
        """

        # Repository URL
        self._documentation_url = "https://github.com/GeorgeCiesinski/text-script"
        _documentation_message = f"""You can find the documentation at the below link: 

{self._documentation_url}

"""

        # Creates a new window
        self._doc_window = tk.Tk()

        # Window setup
        self._doc_window.title("Text-Script Documentation")
        self._doc_window.iconbitmap(default='../assets/textscript.ico')  # Sets the window corner icon
        self._doc_window.geometry("310x130")

        # Create Labels
        _link_label = tk.Label(
            self._doc_window,
            justify="left",
            text=_documentation_message
        )

        # Create Buttons
        _open_link = tk.Button(
            self._doc_window,
            text="Open Link",
            width=11,
            height=1,
            bd=4,
            command=self._open_link
        )

        # Packs widgets into window
        # Labels
        _link_label.grid(row=1, column=0, padx=4, pady=2)
        # Buttons
        _open_link.grid(row=2, column=0)

    def _open_link(self):
        """
        Opens documentation link in default browser.
        """

        # Opens link after user presses yes. Opens as a tab and raises the window
        webbrowser.open(self._documentation_url, new=0, autoraise=True)

        # Calls function to close window
        self._close_window()

    def _close_window(self):
        """
        Destroys the documentation window.
        """

        self._doc_window.destroy()

    def _do_nothing(self):
        """
        Temporary placeholder function. To be removed once GUI elements are complete.
        """

        pass

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

    def _on_closing(self):
        """
        Closes program if user clicks x button on the window
        """

        self._log.debug("User clicked the x button. Quiting program.")
        self.close_text_script()

    def close_text_script(self, event=None):
        """
        Kills the GUI. Can be called from outside Gui so Listener can kill it.
        """

        self._word_catcher.stop_listener()
        self._log.debug("Gui: Listener stopped successfully. Destroying the window.")
        self._root.destroy()
