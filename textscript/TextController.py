import sys
from chardet import detect
from pynput.keyboard import Controller, Key, Listener
import pyperclip
from Logger import Logger
from ConfigUtils import Setup
from ConfigUtils import Update


# Class catches individual words as they are typed
class WordCatcher:

    def __init__(self, _log, _keyboard, _shortcut_list, _file_dir_list, _version):

        # Creates instance wide log object
        self._log = _log.log

        self._log.debug("TextController: Starting WordCatcher initialization.")

        # Creates instance wide Setup object
        self._setup = Setup(_log, _version)

        self._log.debug("TextController: Successfully initialized new Setup object in WordCatcher.")
        # Todo: Will passing the setup object work to save from new object being initialized?

        # Creates instance wide Update object
        self._update = Update(_log)

        self._log.debug("TextController: Successfully initialized new Update object in WordCatcher.")
        # Todo: Will passing the update object work to save from new object being initialized?

        # Creates instance wide keyboard variable
        self._keyboard = _keyboard

        # Delimiter
        self._shortcut_delimiter = "#"
        self._command_delimiter = "!"

        # List of Text-Script commands
        self._commands = [
            "!help",
            "!exit",
            "!reload"
        ]

        # Creates instance wide shortcut_list & file_dir_list
        self._shortcut_list = _shortcut_list
        self._file_dir_list = _file_dir_list

        # Temporary word variables
        self._word_in_progress = False  # There is a word currently being built
        self._current_word = ""  # The current word
        self._is_command = False  # Is this word a command

        # Current key and KeyData
        self._key = None
        self._keydata = None

        # Textblock Variable
        self._textblock = ""

        self._log.debug("WordCatcher initialized successfully.")

        # TODO: Look into self.listener.join and why this is even working. Might need to be changed.
        # Start self.listener
        with Listener(on_press=self.word_builder) as self._listener:
            self._listener.join()
            self._log.debug("TextController: Listener started.")

    def word_builder(self, key):
        """
        word_test should listen for the delimiter. If delimiter is pressed, this method should:
        - append following letters to word
        - keep a count of appended letters
        - remove letters when Key.backspace is pressed, and reduce count
        - print word when tab, space, or backspace is pressed
        - delete word after it is printed

        :param key:
        """

        # Sets keypress to instance key value
        self._key = key

        # Converts to raw value string
        self._keycode_to_keydata()

        # Prints keys to console -- debugging
        # print(self._keydata)

        # Checks delimiter
        self._check_delimiter()

        # Checks if word has ended
        self._check_word_end()

        # Checks for backspace
        self._check_backspace()

        # Appends letter if word is in progress
        self._append_letter()

    def _keycode_to_keydata(self):
        """
        Converts KeyCode to string and strips quotations (into variable: keydata).
        """

        # Converts KeyData to string, strips ' from result
        self._keydata = str(self._key)
        self._keydata = self._keydata.strip("'")

    def _check_delimiter(self):
        """
        Checks if shortcut or command delimiter has been entered. Either starts self.current_word or restarts it.
        """

        if self._keydata == self._shortcut_delimiter or self._keydata == self._command_delimiter:

            self._is_command = False  # Words are not commands by default

            if self._word_in_progress is True:
                self._log.debug("TextController: Delimiter detected while word in progress. Restarting word.")
            else:
                self._log.debug("TextController: Delimiter detected. Starting new word.")

            self._clear_current_word()

            # Sets word_in_progress to True as new word has been started
            self._word_in_progress = True

            # Sets _is_command to true if _command_delimiter is detected.
            if self._keydata == self._command_delimiter:
                self._is_command = True

    def _check_word_end(self):
        """
        Checks if Key.tab, Key.space, or Key.enter is pressed. Prints word if pressed.
        """

        if self._keydata == "Key.tab" or self._keydata == "Key.space" or self._keydata == "Key.enter":

            # Checks if there is a word in progress, clears it if true
            if self._word_in_progress is True:

                self._log.debug(f"TextController: Word ended by {self._keydata}: {self._current_word}")

                self._check_shortcut()

                # Clears current word
                self._clear_current_word()

    def _check_backspace(self):
        """
        Checks if backspace was pressed. Erases last letter if pressed.
        """

        if self._keydata == "Key.backspace":

            # Removes last letter from word
            self._current_word = self._current_word[:-1]

            self._log.debug("TextController: Key.backspace detected.")

    def _append_letter(self):
        """
        Appends the letter to self.current_word if self.word_in_progress is true
        """

        if self._word_in_progress is True and len(self._keydata) == 1:

            # Adds letter to the word
            self._current_word += self._keydata

            self._log.debug(f"TextController: Appended {self._keydata} to the current word.")

    def _check_shortcut(self):
        """
        Checks list of shortcuts for a match. Sets text block if match is found.
        """

        self._log.debug(f"TextController: Checking the shortcut {self._current_word}.")

        # If shortcut is in command list, determine which command was used
        if self._current_word in self._commands:

            self._determine_command()

        # If shortcut is in shortcut_list, determine which shortcut was used
        if self._current_word in self._shortcut_list:

            # Finds index of self.current_word on shortcut list
            shortcut_index = self._shortcut_list.index(self._current_word)

            # Passes the above index to self.read_textblock
            self._find_file_directory(shortcut_index)

            # Update history
            self._update.update_history(self._current_word, self._textblock)

            # Deletes the typed out shortcut
            self._keyboard.delete_shortcut(self._current_word)

            # Passes the textbox to the keyboard
            self._keyboard.paste_block(self._textblock)

    def _determine_command(self):

        # Exit program if user typed in #exit
        if self._current_word == "!exit":

            self._log.debug("The user has typed #exit. Exiting program.")
            self._exit_program()

        # Paste help menu if user typed in #help
        if self._current_word == "!help":

            self._log.debug("The user has typed in #help. Pasting help menu.")
            self._help_menu()

        if self._current_word == "!reload":

            self._log.debug("The user has typed in #reload. Reloading shortcut_list and file_dir_list.")
            self._reload_shortcuts()

    def _reload_shortcuts(self):
        """
        Reloads the shortcuts without restarting the program.
        """

        # Gets a list with default, local, and remote directories
        directories = self._setup.find_directories()

        # Load shortcuts and file directories
        self._shortcut_list, self._file_dir_list = self._setup.shortcut_setup(directories)

        # Check if new shortcuts have been added
        self._setup.new_shortcut_check(self._shortcut_list)

        reload_text = "Shortcuts Reloaded."

        self._log.info("TextController: Shortcuts Reloaded.")

        self._keyboard.delete_shortcut(self._current_word)

        self._keyboard.paste_block(reload_text)

    def _exit_program(self):
        """
        Exits the program.
        """

        exit_text = "Text-Script exited."

        self._keyboard.delete_shortcut(self._current_word)

        self._keyboard.paste_block(exit_text)

        # Close the program with no error
        sys.exit(0)

    def _help_menu(self):

        _help_text = """Help Menu:

How to make a shortcut:

1. Navigate to the program folder, and go to the Textblocks folder
2. Either navigate to an existing folder in Textblocks, or create a new one
3. Create a new text file here. The naming convention is #____.txt where ____ is the shortcut you will type
4. Open the text file and put your text block / signature / template in here
5. Click "Save As" and select the same text file, but change encoding to unicode

Note: Other formats may still work, but this is designed to read unicode text files.

To reload shortcuts, type: !reload
To exit Text-Script, type: !exit"""

        self._keyboard.delete_shortcut(self._current_word)

        self._keyboard.paste_block(_help_text)

    def _find_file_directory(self, index):
        """
        Finds the directory of the Textblock file.
        """

        # Searches self.file_dir_list by index for the directory
        _textblock_directory = self._file_dir_list[index]
        self._log.debug(f"TextController: Successfully found the textblock directory: {_textblock_directory}")

        # Reads the textblock file
        self._read_textblock(_textblock_directory)

    def _read_textblock(self, _textblock_directory):
        """
        Reads the file located in textblock_directory.
        """

        # Chardet attempts to guess the file encoding
        try:
            _chardet_result = detect(open(_textblock_directory, "rb").read())
            self._log.debug(f"TextController: Chardet encoding guess: {_chardet_result}")

            _encoding = _chardet_result['encoding']

        except Exception:
            self._log.debug("TextController: Failed to guess the encoding using Chardet.")
            raise

        except FileNotFoundError:
            self._log.debug("TextController: Textblock location cannot be found. Please check if the shortcut still exists.")
            raise

        else:

            self._log.debug("TextController: Successfully guessed the textblock encoding.")

            # Attempt to open file in UTF-16
            try:
                # Opens the textblock directory
                with open(_textblock_directory, mode="r", encoding=_encoding) as t:

                    # Assigns textblock content to the variable
                    self._textblock = t.read()
            except FileNotFoundError:
                self._log.exception("Unable to open textblock as the file is missing.")
                raise
            except UnicodeDecodeError:
                self._log.exception(f"Failed to open file in {_encoding} encoding. Try changing the textblock encoding to Unicode.")
                raise
            else:
                self._log.debug(f"Successfully opened the file in {_encoding} encoding.")
                return

    def _clear_current_word(self):
        """
        Replaces self.current_word with empty string, and sets self.word_in_progress to False
        """

        self._current_word = ""
        self._word_in_progress = False

        self._log.debug("TextController: Cleared current word & self.current_word changed to False.")


class KeyboardEmulator:

    def __init__(self, _log):

        self._log = _log.log

        self._log.debug("TextController: Starting KeyboardEmulator initialization.")

        # Initializes controller
        self._controller = Controller()

        self._log.debug("Controller initialized.")
        self._log.debug("KeyboardEmulator initialized successfully.")

    def delete_shortcut(self, current_word):
        """
        Deletes the shortcut that the user typed in.
        """

        try:
            word_length = len(current_word)
            for i in range(word_length + 1):
                self._controller.press(Key.backspace)
                self._controller.release(Key.backspace)
        except Exception:
            self._log.exception(f"TextController: Failed to delete the shortcut.{current_word}")
            raise
        else:
            self._log.debug(f"TextController: Successfully deleted the shortcut: {current_word}")

    def paste_block(self, _textblock):
        """
        paste_block copies the textblock into the clipboard and pastes it using pyinput controller.
        """

        # TODO: Determine why pyperclip can't save clipboard item and paste back into clipboard later

        try:

            pyperclip.copy(_textblock)

            # TODO: Look up Pyperclip documentation for OSX & Linux implementation

            # TODO: Test pyperclip.paste()
            self._controller.press(Key.ctrl_l)
            self._controller.press('v')
            self._controller.release(Key.ctrl_l)
            self._controller.release('v')

        except Exception:

            self._log.exception("TextController: Failed to paste the textblock.")
            print("An error has occurred while pasting the textblock. Please see the logs for more detail.")
            # Todo: What is the behavior if we do not raise this?

        else:
            self._log.debug("TextController: Successfully pasted the textblock.")


if __name__ == "__main__":

    # Creates instance of Logger
    L = Logger()
    L.log.debug("Program started from TextController.py. Debugging.")

    # Initializes KeyboardEmulator instance
    k = KeyboardEmulator(L)

    # Initializes WordCatcher instance
    w = WordCatcher(L, k)
