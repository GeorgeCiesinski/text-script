import sys
from pynput.keyboard import Controller, Key, Listener
import pyperclip
from Logger import Logger


# Class catches individual words as they are typed
class WordCatcher:

    def __init__(self, log, keyboard, shortcut_list, file_dir_list):

        # Creates instance wide log variable
        self.log = log.log

        # Creates instance wide keyboard variable
        self.keyboard = keyboard

        # Creates instance wide shortcut_list & file_dir_list
        self.shortcut_list = shortcut_list
        self.file_dir_list = file_dir_list

        # Temporary word variable
        self.word_in_progress = False
        self.current_word = ""

        # Current key and KeyData
        self.key = None
        self.keydata = None

        # Delimiter
        self.delimiter = "#"

        # Textblock Variable
        self.textblock = ""

        self.log.debug("WordCatcher initialized.")

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
        self.key = key

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
        self.keydata = str(self.key)
        self.keydata = self.keydata.strip("'")

    def check_delimiter(self):
        """
        Checks if delimiter has been entered. Either starts self.current_word or restarts it.
        """

        # If delimiter is entered but there is a word in progress, clear the word and start a new word
        if self.keydata == self.delimiter and self.word_in_progress is True:

            self.clear_current_word()

            # Sets word_in_progress to True as new word has been started
            self.word_in_progress = True

            self.log.debug("Delimiter detected while word in progress. Restarting word.")

        # If delimiter is entered and there is no word in progress, start a new word
        elif self.keydata == self.delimiter and self.word_in_progress is False:

            self.word_in_progress = True

            self.log.debug("Delimiter detected. Starting new word.")

    def check_word_end(self):
        """
        Checks if Key.tab, Key.space, or Key.enter is pressed. Prints word if pressed.
        """

        if self.keydata == "Key.tab" or self.keydata == "Key.space" or self.keydata == "Key.enter":

            # Checks if there is a word in progress, clears it if true
            if self.word_in_progress is True:

                self.check_shortcut()

                self.log.debug(f"Word ended by {self.keydata}: {self.current_word}")

                # Clears current word
                self.clear_current_word()

    def check_backspace(self):
        """
        Checks if backspace was pressed. Erases last letter if pressed.
        """

        if self.keydata == "Key.backspace":

            # Removes last letter from word
            self.current_word = self.current_word[:-1]

            self.log.debug("Key.backspace entered, removing last letter from word. The current word is:")
            self.log.debug(self.current_word)

    def append_letter(self):
        """
        Appends the letter to self.current_word if self.word_in_progress is true
        """

        if self.word_in_progress is True and len(self.keydata) == 1:

            # Adds letter to the word
            self.current_word += self.keydata

            self.log.debug(f"Appended {self.keydata} to the current word.")

    def check_shortcut(self):
        """
        Checks list of shortcuts for a match. Sets text block if match is found.
        """

        # Exit program if user typed in #exit
        if self.current_word == "#exit":

            exit_text = "Text-Script exited."

            self.keyboard.delete_shortcut(self.current_word)

            self.keyboard.paste_block(exit_text)

            self.log.debug("The user has typed #exit. Exiting program.")

            # Close the program with no error
            sys.exit(0)

        if self.current_word in self.shortcut_list:

            # Finds index of self.current_word on shortcut list
            shortcut_index = self.shortcut_list.index(self.current_word)

            # Passes the above index to self.read_textblock
            self.find_file_directory(shortcut_index)

            # Deletes the typed out shortcut
            self.keyboard.delete_shortcut(self.current_word)

            # Passes the textbox to the keyboard
            self.keyboard.paste_block(self.textblock)

    def find_file_directory(self, index):
        """
        Finds the directory of the Textblock file.
        """

        # Searches self.file_dir_list by index for the directory
        textblock_directory = self.file_dir_list[index]
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
                self.textblock = f.read()
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
                self.textblock = f.read()
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

        self.current_word = ""
        self.word_in_progress = False

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

        try:
            pyperclip.copy(textblock)

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
