from Logger import Logger
from TextController import WordCatcher, KeyboardEmulator

# Initialize Logger
L = Logger()
L.log.debug("Program started from App.py.")

# Initializes KeyboardEmulator instance
k = KeyboardEmulator(L)

# Initialize WordCatcher
w = WordCatcher(L, k)
