from pynput.keyboard import Listener


# Class catches individual words as they are typed
class WordCatcher:

    def __init__(self):

        # Temporary word variable
        self.word_in_progress = False
        self.current_word = ""

        # Current key and KeyData
        self.key = None
        self.keydata = None

        # Delimiter
        self.delimiter = "#"

        print("WordCatcher has been initialized.")

    def word_builder(self, key):
        """
        word_test should listen for the delimiter. If delimiter is pressed, this method should:
        - append following letters to word
        - keep a count of appended letters
        - remove letters when Key.backspace is pressed, and reduce count
        - print word when tab, space, or backspace is pressed
        - delete word after it is printed

        :param key:
        :return:
        """

        # Sets keypress to instance key value
        self.key = key

        # Converts to raw value string
        self.keycode_to_keydata()

        # Checks delimiter
        self.delimiter_check()

        # Checks if word has ended
        self.word_end_check()

        # Appends letter if word is in progress
        self.letter_append()

    def keycode_to_keydata(self):
        """
        Converts KeyCode to raw key value.
        """

        # Converts KeyData to string, strips ' from result
        self.keydata = str(self.key)
        self.keydata = self.keydata.strip("'")

        print(self.keydata)

    def delimiter_check(self):
        """
        Checks if delimiter has been entered
        """

        if self.keydata == self.delimiter and self.word_in_progress is True:
            # If delimiter is entered but there is a word in progress, clear the word and start anew
            self.clear_current_word()
            self.word_in_progress = True

            print("Delimiter has been detected while word in progress.")
        elif self.keydata == self.delimiter and self.word_in_progress is False:
            # If delimiter is entered, start a new word
            self.word_in_progress = True
            print("Delimiter has been detected. Word in progress set to True.")

    def word_end_check(self):
        """
        Checks if Key.tab, Key.space, or Key.enter is pressed. Prints word if pressed.
        """

        if self.keydata == "Key.tab" or self.keydata == "Key.space" or self.keydata == "Key.enter":
            print(self.current_word)
            self.clear_current_word()

            print("Word has ended.\n")

    def letter_append(self):
        """
        Appends the letter to self.current_word if self.word_in_progress is true
        """

        if self.word_in_progress is True:
            self.current_word += self.keydata
            print(f"Appended {self.keydata} to self.current_word.")

    def clear_current_word(self):

        self.current_word = ""
        self.word_in_progress = False

        print("Clearing current word.")


# Creates instance of WordCatcher
w = WordCatcher()

# Starting listener
with Listener(on_press=w.word_builder) as listener:
    listener.join()
