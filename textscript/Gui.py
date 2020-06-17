import glib
import threading
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox


class Gui:

    def __init__(self, _word_catcher, _log, _setup):

        # Creates instance wide log object
        self._log = _log.log
        self._log.debug("Gui: Starting Gui initialization.")

        # Imports WordCatcher object initialized in text-script
        self._word_catcher = _word_catcher

        # Imports Setup object initialized in text-script
        self._setup = _setup

        # Sends the self object to TextController so the Tkinter window can be closed
        self._word_catcher.set_gui(self)

        # Initialize root in __init__
        self._root = None

        # Threading event: used for communication between threads
        self._stop_event = threading.Event()

        # Global Font Settings
        # Category Font: Bold and larger than regular font
        self._font_category = "Helvetica 12 bold"
        # Regular Font
        self._font_regular = "Helvetica"
        # Bold Font
        self._font_bold = "Helvetica 10 bold"
        # Monospace Font
        self._mono_font = "TkFixedFont"

        # Sets up the window layout
        self._setup_root_window()

        # Starts WordCatcher listener
        self._start_word_catcher()
        self._log.debug("Gui: WordCatcher started successfully.")

        # Close program if window is destroyed
        self._root.protocol("WM_DELETE_WINDOW", self._on_closing)

        self._log.debug("Gui: Initialization complete.")

        # Starts the window loop
        self._log.debug("Gui: Starting root mainloop.")
        self._root.mainloop()

    def _setup_root_window(self):
        """
        Window Setup
        """

        self._log.debug("Gui: Setting up root window.")

        # Creates the root window
        self._root = tk.Tk()

        # Prevents window from being resizable
        self._root.resizable(False, False)

        # Sets the window corner icon
        self._root.iconbitmap(default='../assets/textscript.ico')

        # Window title
        self._root.title("Text-Script")

        # Window size
        # self._root.geometry("400x400")

        # Create menu
        self._create_menu()

        # Create the Info frames
        self._create_stats_frame()
        self._create_textblock_frame()
        self._create_new_shortcuts_frame()
        self._create_removed_shortcuts_frame()
        self._create_buttons_frame()

        # Place Info Frames
        self._organize_frames()

        self._log.debug("Root window setup successfully.")

    """
    Menu and Menu Widgets
    """

    def _create_menu(self):

        self._log.debug("Gui: Setting up top menu.")

        # Create menu object
        _menu = tk.Menu(self._root)
        self._root.config(menu=_menu)

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
        _help_menu.add_command(
            label="Report a Bug",
            command=self._do_nothing
        )

        # Shortcuts for menu options
        self._root.bind_all("<Control-q>", self.close_text_script)
        self._root.bind_all("<Control-h>", self._do_nothing())

        self._log.debug("Gui: Successfully created top menu.")

    def _create_stats_frame(self):
        """
        Creates a new frame for the stats labels
        """

        self._log.debug("Gui: Creating the stats frame.")

        # Create the frame
        self._stats_frame = tk.Frame(self._root)

        # Create Information Labels
        _your_stats_label = tk.Label(
            self._stats_frame,
            font=self._font_category,
            text="YOUR STATS:"
        )
        _shortcuts_label = tk.Label(
            self._stats_frame,
            text="Shortcuts Used: "
        )
        _characters_typed_label = tk.Label(
            self._stats_frame,
            text="Shortcut characters typed: "
        )
        _characters_pasted_label = tk.Label(
            self._stats_frame,
            text="Textblock characters pasted: "
        )
        _keystrokes_saved_label = tk.Label(
            self._stats_frame,
            text="Keystrokes saved: "
        )
        _time_to_copy_paste_label = tk.Label(
            self._stats_frame,
            text="Time to copy and paste: "
        )
        _total_time_saved_label = tk.Label(
            self._stats_frame,
            text="Total amount of time saved: "
        )

        # Get Stats
        _stats = self._setup.get_stats()
        _complete_stats = self._setup.calculate_stats(_stats)

        # Create StringVars
        self._shortcuts_sv = tk.StringVar(self._stats_frame, value=_complete_stats[0])
        self._shortcut_chars_sv = tk.StringVar(self._stats_frame, value=_complete_stats[1])
        self._textblock_chars_sv = tk.StringVar(self._stats_frame, value=_complete_stats[2])
        self._saved_keystrokes_sv = tk.StringVar(self._stats_frame, value=_complete_stats[3])
        self._seconds_paste_sv = tk.StringVar(self._stats_frame, value=_complete_stats[4])
        self._time_saved_sv = tk.StringVar(self._stats_frame, value=_complete_stats[5])

        # Updates StringVars
        self.update_stats_frame()

        # Create StringVar Labels
        _shortcuts = tk.Entry(
            self._stats_frame,
            state="disabled",
            textvariable=self._shortcuts_sv
        )
        _characters_typed = tk.Entry(
            self._stats_frame,
            state="disabled",
            textvariable=self._shortcut_chars_sv
        )
        _characters_pasted = tk.Entry(
            self._stats_frame,
            state="disabled",
            textvariable=self._textblock_chars_sv
        )
        _keystrokes_saved = tk.Entry(
            self._stats_frame,
            state="disabled",
            textvariable=self._saved_keystrokes_sv
        )
        _time_to_copy_paste = tk.Entry(
            self._stats_frame,
            state="disabled",
            textvariable=self._seconds_paste_sv
        )
        _total_time_saved = tk.Entry(
            self._stats_frame,
            state="disabled",
            textvariable=self._time_saved_sv
        )

        # Pack Widgets
        # Info Labels
        _your_stats_label.grid(column=0, row=0, columnspan=2, sticky="w")
        _shortcuts_label.grid(column=0, row=1, sticky="w")
        _characters_typed_label.grid(column=0, row=2, sticky="w")
        _characters_pasted_label.grid(column=0, row=3, sticky="w")
        _keystrokes_saved_label.grid(column=0, row=4, sticky="w")
        _time_to_copy_paste_label.grid(column=0, row=5, sticky="w")
        _total_time_saved_label.grid(column=0, row=6, sticky="w")
        # StringVar Fields
        _shortcuts.grid(column=1, row=1, sticky="w")
        _characters_typed.grid(column=1, row=2, sticky="w")
        _characters_pasted.grid(column=1, row=3, sticky="w")
        _keystrokes_saved.grid(column=1, row=4, sticky="w")
        _time_to_copy_paste.grid(column=1, row=5, sticky="w")
        _total_time_saved.grid(column=1, row=6, sticky="w")

        self._log.debug("Gui: Successfully setup the stats frame.")

    def update_stats_frame(self):
        """
        Updates the StringVars, which immediately updates the labels
        """

        self._log.debug("Gui: Updating stats frame.")

        # Get Stats
        _stats = self._setup.get_stats()
        _complete_stats = self._setup.calculate_stats(_stats)

        # Create StringVars
        self._shortcuts_sv.set(_complete_stats[0])
        self._shortcut_chars_sv.set(_complete_stats[1])
        self._textblock_chars_sv.set(_complete_stats[2])
        self._saved_keystrokes_sv.set(_complete_stats[3])
        self._seconds_paste_sv.set(_complete_stats[4])
        self._time_saved_sv.set(_complete_stats[5])

        self._log.debug("Gui: Successfully updated stats frame.")

    def _create_textblock_frame(self):
        """
        Creates a new frame for the stats labels
        """

        self._log.debug("Gui: Creating the textblock frame.")

        # Directories, shortcuts, file dirs
        _directories = self._setup.find_directories()
        _shortcut_list, _file_dir_list = self._setup.shortcut_setup(_directories)

        # Get longest shortcut
        _max_shortcut_len = len(max(_shortcut_list, key=len))
        _shortcut_len_allowance = _max_shortcut_len + 1

        # Create the frame
        self._textblock_frame = tk.Frame(self._root)

        # Create Information Label
        _textblocks_label = tk.Label(
            self._textblock_frame,
            font=self._font_category,
            text="TEXTBLOCKS:"
        )

        # Scrollbars
        _vertical_scrollbar = tk.Scrollbar(
            self._textblock_frame
        )
        _horizontal_scrollbar = tk.Scrollbar(
            self._textblock_frame,
            orient="horizontal"
        )

        # Create Textblock Listbox
        _textblocks_listbox = tk.Listbox(
            self._textblock_frame,
            yscrollcommand=_vertical_scrollbar.set,
            xscrollcommand=_horizontal_scrollbar.set,
            bd=4,
            width=100,
            font=self._mono_font,
            relief="groove",
            selectmode="single"
        )

        _vertical_scrollbar.config(command=_textblocks_listbox.yview)
        _horizontal_scrollbar.config(command=_textblocks_listbox.xview)

        for _shortcut in _shortcut_list:

            # Get shortcut index
            _shortcut_index = _shortcut_list.index(_shortcut)
            # Get filedir for above index
            _file_dir = _file_dir_list[_shortcut_index]

            # Create list item
            _list_item = _shortcut

            # Adds spaces to fill up max allowance
            _shortcut_length = len(_shortcut)
            _add_spaces = _shortcut_len_allowance - _shortcut_length
            for _spaces in range(_add_spaces):
                _list_item += " "
            _list_item += f" - Directory: {_file_dir}"

            # Add item to listbox
            _textblocks_listbox.insert((_shortcut_index + 1), _list_item)

        # Pack Widgets
        # Info Labels
        _textblocks_label.grid(column=0, row=0, columnspan=2, sticky="w")
        # Listbox & scrollbar
        _textblocks_listbox.grid(column=0, row=1, sticky="w")
        _vertical_scrollbar.grid(column=1, row=1, sticky="ns")
        _horizontal_scrollbar.grid(column=0, row=2, sticky="ew")

    def _create_new_shortcuts_frame(self):
        """
        Creates a new frame for the new shortcuts
        """

        self._log.debug("Gui: Creating the New Shortcuts frame.")

        # Create the frame
        self._new_shortcuts_frame = tk.Frame(self._root)

        # Create Information Label
        _new_shortcuts_label = tk.Label(
            self._new_shortcuts_frame,
            font=self._font_category,
            text="NEW SHORTCUTS:"
        )

        # Create Textblock Listbox
        _new_shortcuts_listbox = tk.Listbox(
            self._new_shortcuts_frame,
            bd=4,
            font=self._mono_font,
            selectmode="single",
            relief="groove",
            height=5,
            width=30
        )

        _new_shortcut_list = self._setup.new_shortcuts

        for _shortcut in _new_shortcut_list:
            _shortcut_index = _new_shortcut_list.index(_shortcut)
            _new_shortcuts_listbox.insert((_shortcut_index + 1), _shortcut)

        # Pack Widgets
        # Info Labels
        _new_shortcuts_label.grid(column=0, row=0, sticky="w")
        # Listbox & scrollbar
        _new_shortcuts_listbox.grid(column=0, row=1, sticky="w")

    def _create_removed_shortcuts_frame(self):
        """
        Creates a new frame for the removed shortcuts
        """

        self._log.debug("Gui: Creating the Removed Shortcuts frame.")

        # Create the frame
        self._removed_shortcuts_frame = tk.Frame(self._root)

        # Create Information Label
        _removed_shortcuts_label = tk.Label(
            self._removed_shortcuts_frame,
            font=self._font_category,
            text="REMOVED SHORTCUTS:"
        )

        # Create Textblock Listbox
        _removed_shortcuts_listbox = tk.Listbox(
            self._removed_shortcuts_frame,
            bd=4,
            font=self._mono_font,
            selectmode="single",
            relief="groove",
            height=5,
            width=30
        )

        _removed_shortcut_list = self._setup.removed_shortcuts

        for _shortcut in _removed_shortcut_list:
            _shortcut_index = _removed_shortcut_list.index(_shortcut)
            _removed_shortcuts_listbox.insert((_shortcut_index + 1), _shortcut)

        # Pack Widgets
        # Info Labels
        _removed_shortcuts_label.grid(column=0, row=0, sticky="w")
        # Listbox & scrollbar
        _removed_shortcuts_listbox.grid(column=0, row=1, sticky="w")

    def _create_buttons_frame(self):
        """
        Creates a new frame containing the button controls
        """

        self._log.debug("Gui: Creating the buttons frame.")

        # Create the frame
        self._buttons_frame = tk.Frame(self._root)

        _add_button = tk.Button(
            self._buttons_frame,
            text="Add",
            width=10,
            command=self._add_new_textblock
        )

        _edit_button = tk.Button(
            self._buttons_frame,
            text="Edit",
            width=10,
            command=self._edit_textblock
        )

        _delete_button = tk.Button(
            self._buttons_frame,
            text="Delete",
            width=10,
            command=self._delete_textblock
        )

        _add_button.grid(column=0, row=0, sticky="nw", padx="2", pady="2")
        _edit_button.grid(column=1, row=0, sticky="nw", padx="2", pady="2")
        _delete_button.grid(column=2, row=0, sticky="nw", padx="2", pady="2")

    def _organize_frames(self):
        """
        Organizes frames and widgets in root frame
        """

        self._textblock_frame.grid(column=0, row=0, rowspan=2, columnspan=3, padx="3", pady="1", sticky="nw")
        self._stats_frame.grid(column=2, row=2, rowspan=2, padx="3", pady="1", sticky="nw")
        self._new_shortcuts_frame.grid(column=0, row=2, padx="3", pady="1", sticky="nw")
        self._removed_shortcuts_frame.grid(column=1, row=2, padx="3", pady="1", sticky="nw")
        self._buttons_frame.grid(column=0, row=3, padx="3", pady="1", sticky="nw")

    def _open_settings(self):
        """
        Opens a window with the available settings. Alters the config file.
        """

        # Get the directories from config file
        _directories = self._setup.find_directories()

        # Sets the entry values
        if (_directories[0] is None) or (len(_directories[0]) == 0):
            _current_default = "Not Set"
        else:
            _current_default = _directories[0]

        if (_directories[1] is None) or (len(_directories[1]) == 0):
            _current_local = "Not Set"
        else:
            _current_local = _directories[1]

        if (_directories[2] is None) or (len(_directories[2]) == 0):
            _current_remote = "Not Set"
        else:
            _current_remote = _directories[2]

        """
        Create Window
        """

        # Creates a new window
        self._settings_window = tk.Toplevel()
        self._log.debug("Gui: Settings window created successfully.")

        # Window Setup
        self._settings_window.title("Settings")
        self._settings_window.iconbitmap(default='../assets/textscript.ico')  # Sets the window corner icon
        self._log.debug("Successfully setup settings window.")

        """
        Create Widgets
        """

        # Static Labels
        _directories_label = tk.Label(
            self._settings_window,
            justify="left",
            text="DIRECTORIES",
            font=self._font_category
        )
        _default_label = tk.Label(
            self._settings_window,
            justify="left",
            text="Default Directory: "
        )
        _local_label = tk.Label(
            self._settings_window,
            justify="left",
            text="Local Directory: "
        )
        _remote_label = tk.Label(
            self._settings_window,
            justify="left",
            text="Remote Directory: ",
        )
        # Save Result Label - shows the result of self._save_settings
        self._save_result = tk.Label(
            self._settings_window,
            justify="left",
            fg="red",
            font=self._font_bold,
            text=""
        )

        # TK StringVars (required to change text of entry fields automatically)
        # Entry
        self._default_sv = tk.StringVar(self._settings_window, value=_current_default)
        self._local_sv = tk.StringVar(self._settings_window, value=_current_local)
        self._remote_sv = tk.StringVar(self._settings_window, value=_current_remote)

        # Directory Entry Fields
        self._default_entry = tk.Entry(
            self._settings_window,
            justify="left",
            width=45,
            textvariable=self._default_sv,
        )
        self._local_entry = tk.Entry(
            self._settings_window,
            justify="left",
            width=45,
            textvariable=self._local_sv,
        )
        self._remote_entry = tk.Entry(
            self._settings_window,
            justify="left",
            width=45,
            textvariable=self._remote_sv,
        )

        # Buttons
        # Default
        _btn_enable_default = tk.Button(
            self._settings_window,
            width=11,
            text="Enable",
            command=self._enable_default
        )
        _btn_disable_default = tk.Button(
            self._settings_window,
            width=11,
            text="Disable",
            command=self._disable_default
        )
        # Local
        _btn_set_local = tk.Button(
            self._settings_window,
            width=11,
            text="Set",
            command=self._set_local
        )
        _btn_disable_local = tk.Button(
            self._settings_window,
            width=11,
            text="Disable",
            command=self._disable_local
        )
        # Remote
        _btn_set_remote = tk.Button(
            self._settings_window,
            width=11,
            text="Set",
            command=self._set_remote
        )
        _btn_disable_remote = tk.Button(
            self._settings_window,
            width=11,
            text="Disable",
            command=self._disable_remote
        )
        # Save
        _btn_save = tk.Button(
            self._settings_window,
            width=11,
            text="Save",
            command=self._save_settings
        )

        self._log.debug("Successfully created widgets.")

        # Pack Widgets
        # Description Labels
        _directories_label.grid(row=0, column=0, sticky="w", padx=4, pady=2)
        _default_label.grid(row=1, column=0, sticky="w", padx=4, pady=2)
        _local_label.grid(row=2, column=0, sticky="w", padx=4, pady=2)
        _remote_label.grid(row=3, column=0, sticky="w", padx=4, pady=2)
        # Entry Fields
        self._default_entry.grid(row=1, column=1, sticky="w", padx=4, pady=2)
        self._local_entry.grid(row=2, column=1, sticky="w", padx=4, pady=2)
        self._remote_entry.grid(row=3, column=1, sticky="w", padx=4, pady=2)
        # Buttons
        _btn_enable_default.grid(row=1, column=2, sticky="w", padx=4, pady=2)
        _btn_disable_default.grid(row=1, column=3, sticky="w", padx=4, pady=2)
        _btn_set_local.grid(row=2, column=2, sticky="w", padx=4, pady=2)
        _btn_disable_local.grid(row=2, column=3, sticky="w", padx=4, pady=2)
        _btn_set_remote.grid(row=3, column=2, sticky="w", padx=4, pady=2)
        _btn_disable_remote.grid(row=3, column=3, sticky="w", padx=4, pady=2)
        _btn_save.grid(row=4, column=3, sticky="w", padx=4, pady=2)
        # Save Result
        self._save_result.grid(row=4, column=1, sticky="w", padx=4, pady=2)

        self._log.debug("Successfully placed widgets in the window.")

    def _enable_default(self):
        """
        Sets the default directory in settings menu
        """
        try:
            self._default_sv.set("./textblocks/")
            self._save_result['text'] = ""
            self._settings_window.lift()
        except Exception:
            self._log.exception("Gui: An error has occurred in _enable_default")
        else:
            self._log.debug("Gui: Successfully enabled default directory")


    def _disable_default(self):
        """
        Disables the default directory in settings menu
        """
        try:
            self._default_sv.set("Not Set")
            self._save_result['text'] = ""
            self._settings_window.lift()
        except Exception:
            self._log.exception("Gui: An error has occurred in _disable_default")
        else:
            self._log.debug("Gui: Successfully disabled default directory")

    def _set_local(self):
        """
        Sets local directory in settings menu
        """

        try:
            # Uses askdirectory to set the directory
            self._local_sv.set(filedialog.askdirectory())  # Shows askdirectory dialog, saves result to StringVar
            self._save_result['text'] = ""  # Deletes the save result text
            self._settings_window.lift()  # Lifts the settings window to the front
        except Exception:
            self._log.exception("Gui: An error has occurred in _set_local")
        else:
            self._log.debug("Gui: Successfully set the local directory")

    def _disable_local(self):
        """
        Disables the local directory in settings menu
        """

        try:
            self._local_sv.set("Not Set")
            self._save_result['text'] = ""
            self._settings_window.lift()
        except Exception:
            self._log.exception("Gui: An error has occurred in _disable_local")
        else:
            self._log.debug("Gui: Successfully disabled local directory")


    def _set_remote(self):
        """
        Save remote directory in settings menu
        """

        try:
            # Uses askdirectory to set the directory
            self._remote_sv.set(filedialog.askdirectory())
            self._save_result['text'] = ""
            self._settings_window.lift()
        except Exception:
            self._log.exception("Gui: An error has occurred in _set_remote")
        else:
            self._log.debug("Gui: Successfully set the remote directory")

    def _disable_remote(self):
        """
        Disables the remote directory in settings menu
        """

        try:
            self._remote_sv.set("Not Set")
            self._save_result['text'] = ""
            self._settings_window.lift()
        except Exception:
            self._log.exception("Gui: An error has occurred in _disable_remote")
        else:
            self._log.debug("Gui: Successfully disabled remote directory")

    def _save_settings(self):
        """
        Overwrites the directories in the config file
        """

        # Initialize Variables
        _save_successful = False  # Variable that tracks if save was successful

        # Gets the values from the entry fields
        _default = self._default_entry.get()
        _local = self._local_entry.get()
        _remote = self._remote_entry.get()

        _real_dirs = True  # Tracks if all directories are real before saving
        _error_message = ""

        # Sets values to None if Not Set
        if _default == "Not Set":
            _default = "None"
        if _local == "Not Set":
            _local = "None"
        if _remote == "Not Set":
            _remote = "None"

        _directories = [_default, _local, _remote]  # List of directories

        for _directory in _directories:  # For each directory

            if _directory != "None":
                _exists = glib.check_directory(_directory)  # Check if the directory exists

                if _exists is False:  # If doesn't exist
                    _real_dirs = False  # Set _real_dirs to false, else leave it True
                    _error_message += f"Invalid directory: {_directory}\n"

        if _real_dirs is False:
            messagebox.showinfo("Save settings failed", _error_message)
        else:
            # Writes to config
            print(f"Saving directories: {_default}, {_local}, {_remote}")
            _save_successful = self._setup.save_settings(_directories)

        if _save_successful is True:
            self._log.debug("Successfully saved the settings.")
            self._save_result['text'] = "Save Successful"
            self._word_catcher.reload_shortcuts(called_externally=True)

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
            font=self._font_bold,
            text=_help_text
        )

        # Packs labels into window
        _help_label.grid(row=0, column=0, sticky="w", padx=4, pady=2)

    def _open_documentation(self):
        """
        Shows the user the link to the documentation and offers to open this in browser. Selecting no closes the window.
        """

        # Repository URL
        self._documentation_url = "https://github.com/GeorgeCiesinski/text-script"

        # Label text for documentation window
        _documentation_message = f"""You can find the documentation at the below link: 

{self._documentation_url}

"""

        # Creates a new window
        self._doc_window = tk.Tk()

        # Window setup
        self._doc_window.title("Text-Script Documentation")
        self._doc_window.iconbitmap(default='../assets/textscript.ico')  # Sets the window corner icon
        self._doc_window.geometry("340x130")

        # Create Labels
        _link_label = tk.Label(
            self._doc_window,
            justify="left",
            font=self._font_bold,
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
        self._close_doc_window()

    def _close_doc_window(self):
        """
        Destroys the documentation window.
        """

        self._doc_window.destroy()

    """
    Temporary Methods
    """

    def _add_new_textblock(self):

        """
        Opens a new window where textblocks can be created
        """

        # Creates a new window
        self._new_textblock_window = tk.Toplevel()
        self._log.debug("Gui: New textblock window created successfully.")

        # Window Setup
        self._new_textblock_window.title("New Textblock")
        self._new_textblock_window.iconbitmap(default='../assets/textscript.ico')  # Sets the window corner icon
        self._log.debug("Successfully setup new textblock window.")

        """
        Widgets
        """

        # Labels
        _directory_label = tk.Label(
            self._new_textblock_window,
            justify="left",
            text="Directory",
            font=self._font_category
        )
        _shortcut_label = tk.Label(
            self._new_textblock_window,
            justify="left",
            text="Shortcut",
            font=self._font_category
        )
        _textblock_label = tk.Label(
            self._new_textblock_window,
            justify="left",
            text="Textblock",
            font=self._font_category
        )
        _delimiter_label = tk.Label(
            self._new_textblock_window,
            justify="left",
            text="#",
            width=1,
        )

        # Entry & Text
        _shortcut_entry = tk.Entry(
            self._new_textblock_window,
            justify="left",
            width=55
        )
        _textblock_text = tk.Text(
            self._new_textblock_window,
            width=55,
            height=10,
        )

        # Buttons
        _btn_save = tk.Button(
            self._new_textblock_window,
            width=11,
            text="Save",
            command=self._do_nothing
        )

        # Pack Widgets
        _directory_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=4, pady=2)
        _shortcut_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=4, pady=2)
        _delimiter_label.grid(row=2, column=0, sticky="w", padx=4, pady=2)
        _shortcut_entry.grid(row=2, column=1, sticky="w", padx=4, pady=2)
        _textblock_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=4, pady=2)
        _textblock_text.grid(row=4, column=0, columnspan=2, sticky="w", padx=4, pady=2)
        _btn_save.grid(row=5, column=1, sticky="e", padx=4, pady=2)

    def _edit_textblock(self):

        """
        Opens a new window where a textblock can be edited
        """

        # Creates a new window
        self._edit_textblock_window = tk.Toplevel()
        self._log.debug("Gui: Edit textblock window created successfully.")

        # Window Setup
        self._edit_textblock_window.title("Edit Textblock")
        self._edit_textblock_window.iconbitmap(default='../assets/textscript.ico')  # Sets the window corner icon
        self._log.debug("Successfully setup new textblock window.")

    def _delete_textblock(self):

        """
        Opens a new window where a textblock can be deleted
        """

        # Creates a new window
        self._delete_textblock_window = tk.Toplevel()
        self._log.debug("Gui: Delete textblock window created successfully.")

        # Window Setup
        self._delete_textblock_window.title("Delete Textblock")
        self._delete_textblock_window.iconbitmap(default='../assets/textscript.ico')  # Sets the window corner icon
        self._log.debug("Successfully setup new textblock window.")

    def _do_nothing(self):
        """
        Temporary placeholder function. To be removed once GUI elements are complete.
        """

        pass

    """
    WordCatcher and Threading
    """

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
