import sys
from pynput.keyboard import Controller, Key, Listener
import pyperclip
from Logger import Logger
from ConfigUtils import Update


# Class catches individual words as they are typed
class WordCatcher:

    def __init__(self, log, _keyboard, _shortcut_list, _file_dir_list):

        # Creates instance wide log object
        self.log = log.log

        # Creates instance wide UpdateConfig object
        self.update = Update(log)

        # Creates instance wide keyboard variable
        self._keyboard = _keyboard

        # List of Text-Script commands
        self._commands = [
            "#help",
            "#exit",
            "#reload"
        ]

        # Creates instance wide shortcut_list & file_dir_list
        self._shortcut_list = _shortcut_list
        self._file_dir_list = _file_dir_list

        # Temporary word variable
        self._word_in_progress = False
        self._current_word = ""

        # Current key and KeyData
        self._key = None
        self._keydata = None

        # Delimiter
        self._delimiter = "#"

        # Textblock Variable
        self._textblock = ""

        self.log.debug("WordCatcher initialized.")

        # TODO: Look into self.listener.join and why this is even working. Might need to be changed.
        # Start self.listener
        with Listener(on_press=self.word_builder) as self.listener:
            self.listener.join()
            self.log.debug("Listener started.")

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
        self.keycode_to_keydata()

        # Checks delimiter
        self.check_delimiter()

        # Checks if word has ended
        self.check_word_end()

        # Checks for backspace
        self.check_backspace()

        # Appends letter if word is in progress
        self.append_letter()

    def keycode_to_keydata(self):
        """
        Converts KeyCode to string and strips quotations (into variable: keydata).
        """

        # Converts KeyData to string, strips ' from result
        self._keydata = str(self._key)
        self._keydata = self._keydata.strip("'")

    def check_delimiter(self):
        """
        Checks if delimiter has been entered. Either starts self.current_word or restarts it.
        """

        # If delimiter is entered but there is a word in progress, clear the word and start a new word
        if self._keydata == self._delimiter and self._word_in_progress is True:

            self.clear_current_word()

            # Sets word_in_progress to True as new word has been started
            self._word_in_progress = True

            self.log.debug("Delimiter detected while word in progress. Restarting word.")

        # If delimiter is entered and there is no word in progress, start a new word
        elif self._keydata == self._delimiter and self._word_in_progress is False:

            self._word_in_progress = True

            self.log.debug("Delimiter detected. Starting new word.")

    def check_word_end(self):
        """
        Checks if Key.tab, Key.space, or Key.enter is pressed. Prints word if pressed.
        """

        if self._keydata == "Key.tab" or self._keydata == "Key.space" or self._keydata == "Key.enter":

            # Checks if there is a word in progress, clears it if true
            if self._word_in_progress is True:

                self.check_shortcut()

                self.log.debug(f"Word ended by {self._keydata}: {self._current_word}")

                # Clears current word
                self.clear_current_word()

    def check_backspace(self):
        """
        Checks if backspace was pressed. Erases last letter if pressed.
        """

        if self._keydata == "Key.backspace":

            # Removes last letter from word
            self._current_word = self._current_word[:-1]

            self.log.debug("Key.backspace entered, removing last letter from word. The current word is:")
            self.log.debug(self._current_word)

    def append_letter(self):
        """
        Appends the letter to self.current_word if self.word_in_progress is true
        """

        if self._word_in_progress is True and len(self._keydata) == 1:

            # Adds letter to the word
            self._current_word += self._keydata

            self.log.debug(f"Appended {self._keydata} to the current word.")

    def check_shortcut(self):
        """
        Checks list of shortcuts for a match. Sets text block if match is found.
        """

        # If shortcut is in command list, determine which command was used
        if self._current_word in self._commands:

            self.determine_command()

        # If shortcut is in shortcut_list, determine which shortcut was used
        if self._current_word in self._shortcut_list:

            # Finds index of self.current_word on shortcut list
            shortcut_index = self._shortcut_list.index(self._current_word)

            # Passes the above index to self.read_textblock
            self.find_file_directory(shortcut_index)

            # Deletes the typed out shortcut
            self._keyboard.delete_shortcut(self._current_word)

            # Update history
            self.update.update_history(self._current_word, self._textblock)

            # Passes the textbox to the keyboard
            self._keyboard.paste_block(self._textblock)

    def determine_command(self):

        # Exit program if user typed in #exit
        if self._current_word == "#exit":

            self.log.debug("The user has typed #exit. Exiting program.")
            self.exit_program()

        # Paste help menu if user typed in #help
        elif self._current_word == "#help":

            self.log.debug("The user has typed in #help. Pasting help menu.")
            self.help_menu()

        elif self._current_word == "#reload":

            self.log.debug("The user has typed in #reload. Reloading shortcut_list and file_dir_list.")
            pass

    def exit_program(self):
        """
        Exits the program
        """

        exit_text = "Text-Script exited."

        self._keyboard.delete_shortcut(self._current_word)

        self._keyboard.paste_block(exit_text)

        # Close the program with no error
        sys.exit(0)

    def help_menu(self):

        help_text = """Help Menu:

How to make a shortcut:

1. Navigate to the program folder, and go to the Textblocks folder
2. Either navigate to an existing folder in Textblocks, or create a new one
3. Create a new text file here. The naming convention is #____.txt where ____ is the shortcut you will type
4. Open the text file and put your text block / signature / template in here
5. Click "Save As" and select the same text file, but change encoding to unicode

Note: Other formats may still work, but this is designed to read unicode text files.

To exit Text-Script, type: #exit
"""

        self._keyboard.delete_shortcut(self._current_word)

        self._keyboard.paste_block(help_text)

    def update_shortcuts(self):

        # TODO: Create update_shortcuts method
        pass

    def find_file_directory(self, index):
        """
        Finds the directory of the Textblock file.
        """

        # Searches self.file_dir_list by index for the directory
        textblock_directory = self._file_dir_list[index]
        self.log.debug(f"Successfully found the textblock directory: {textblock_directory}")

        # Reads the textblock file
        self.read_textblock(textblock_directory)

    def read_textblock(self, textblock_directory):
        """
        Reads the file located in textblock_directory.
        """

        #TODO: Guess file encoding

        # Attempt to open file in UTF-16
        try:
            # Opens the textblock directory
            with open(textblock_directory, mode="r", encoding="UTF-16") as f:

                # Assigns textblock content to the variable
                self._textblock = f.read()
        except:
            self.log.exception("Attempted to open file in UTF-16. Unsuccessful.")
        else:
            self.log.debug("Successfully read the textblock using UTF-16.")
            return

        # Attempt to open file in UTF-8
        try:
            # Opens the textblock directory
            with open(textblock_directory, mode="r", encoding="UTF-8") as f:

                # Assigns textblock content to the variable
                self._textblock = f.read()
        except:
            self.log.exception("Attempted to open file in UTF-8. Unsuccessful.")
        else:
            self.log.debug("Successfully read the textblock using UTF-8.")
            return

        # Todo: Attempt to load file in local encoding (ANSI)

    def clear_current_word(self):
        """
        Replaces self.current_word with empty string, and sets self.word_in_progress to False
        """

        self._current_word = ""
        self._word_in_progress = False

        self.log.debug("Cleared current word & self.current_word changed to False.")


class KeyboardEmulator:

    def __init__(self, log):

        self.log = log.log

        self.log.debug("KeyboardEmulator initialized.")

        # Initializes controller
        self.c = Controller()

        self.log.debug("Controller initialized.")

    def delete_shortcut(self, current_word):
        """
        Deletes the shortcut that the user typed in.
        """

        try:
            word_length = len(current_word)
            for i in range(word_length + 1):
                self.c.press(Key.backspace)
                self.c.release(Key.backspace)
        except:
            self.log.exception(f"Failed to delete the shortcut.{current_word}")
            raise
        else:
            self.log.debug(f"Successfully deleted the shortcut: {current_word}")

    def paste_block(self, textblock):
        """
        paste_block copies the textblock into the clipboard and pastes it using pyinput controller.
        """

        # TODO: Determine why pyperclip can't save clipboard item and paste back into clipboard later

        try:
            pyperclip.copy(textblock)

            # TODO: Look up Pyperclip documentation for OSX & Linux implementation

            # TODO: Test pyperclip.paste()
            self.c.press(Key.ctrl_l)
            self.c.press('v')
            self.c.release(Key.ctrl_l)
            self.c.release('v')
        except:
            self.log.exception(f"Failed to paste the textblock: {textblock}")
        else:
            self.log.debug(f"Successfully pasted the textblock: {textblock}")


if __name__ == "__main__":

    # Creates instance of Logger
    L = Logger()
    L.log.debug("Program started from TextController.py. Debugging.")

    # Initializes KeyboardEmulator instance
    k = KeyboardEmulator(L)

    # Initializes WordCatcher instance
    w = WordCatcher(L, k)
