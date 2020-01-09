import glib
from Logger import Logger
from TextController import WordCatcher, KeyboardEmulator

# Initialize Logger
L = Logger()

L.log.debug("Program started from App.py.")

# Gets file_list and file_dir_list
textblock_dir = "Textblocks/"

file_list, file_dir_list = glib.list_files(textblock_dir)

# Creates shortcut list with the same index
shortcut_list = glib.list_shortcuts(file_list)

# Initializes KeyboardEmulator instance
k = KeyboardEmulator(L)

# Initialize WordCatcher
w = WordCatcher(L, k, shortcut_list, file_dir_list)
