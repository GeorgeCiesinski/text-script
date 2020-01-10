import glib
from Logger import Logger
from Gui import Gui
from TextController import WordCatcher, KeyboardEmulator

# Initialize Logger
L = Logger()

L.log.debug("Program started from App.py.")

# Gets file_list and file_dir_list
textblock_dir = "Textblocks/"

file_list, file_dir_list = glib.list_files(textblock_dir)

# Creates shortcut list with the same index
shortcut_list = glib.list_shortcuts(file_list)

# Create GUI object
g = Gui(L)

# Initializes KeyboardEmulator instance
k = KeyboardEmulator(L)

# Initialize WordCatcher
w = WordCatcher(L, k, shortcut_list, file_dir_list)

# Close program if window is destroyed
g.root.protocol("WM_DELETE_WINDOW", g.on_closing)

# Tkinter main loop
L.log.debug("Starting Tkinter mainloop.")
g.root.mainloop()
