from pynput.keyboard import Controller, Key, Listener
from Logger import Logger


# Class catches individual words as they are typed
class WordCatcher:

    def __init__(self, log, keyboard):

        # Creates instance wide log variable
        self.log = log.log

        # Creates instance wide typer variable
        self.keyboard = keyboard

        # Temporary word variable
        self.word_in_progress = False
        self.current_word = ""

        # Current key and KeyData
        self.key = None
        self.keydata = None

        # Delimiter
        self.delimiter = "#"

        self.log.debug("WordCatcher has been initialized.")

        # Start listener
        with Listener(on_press=self.word_builder) as listener:
            listener.join()
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

        # Prints typed letter to console
        print(self.keydata)

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

            self.log.debug("Key.backspace entered, removing last letter from word.")

    def append_letter(self):
        """
        Appends the letter to self.current_word if self.word_in_progress is true
        """

        if self.word_in_progress is True and len(self.keydata) == 1:

            # Adds letter to the word
            self.current_word += self.keydata

            self.log.debug(f"Appended {self.keydata} to self.current_word.")

    def check_shortcut(self):
        """
        Checks list of shortcuts for a match. Sets text block if match is found.
        """

        if self.current_word == "#fuck":

            self.keyboard.delete_shortcut(self.current_word)
            self.keyboard.type_block()

    def clear_current_word(self):
        """
        Replaces self.current_word with empty string, and sets self.word_in_progress to False
        """

        self.current_word = ""
        self.word_in_progress = False

        self.log.debug("self.current_word changed to False.")


class KeyboardEmulator:

    def __init__(self, log):

        # Initializes controller
        self.c = Controller()

    def delete_shortcut(self, current_word):
        """
        Deletes the shortcut that the user typed in.
        """

        word_length = len(current_word)
        for i in range(word_length + 1):
            self.c.press(Key.backspace)
            self.c.release(Key.backspace)

    def type_block(self):

        self.c.type("Eat a bag of dicks motherfucker, and FUCK you!")


if __name__ == "__main__":

    # Creates instance of Logger
    L = Logger()
    L.log.debug("Program started from TextController.py. Debugging.")

    # Initializes KeyboardEmulator instance
    k = KeyboardEmulator(L)

    # Initializes WordCatcher instance
    w = WordCatcher(L, k)
