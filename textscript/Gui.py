import tkinter
from Logger import Logger


class Gui:

	def __init__(self, log):

		# Instance wide log variable
		self.log = log.log

		# Instance wide root variable
		self.root = None

		# Creates a new window
		self.create_window()

		# TODO: Create menu

	def create_window(self):

		"""
		create_window creates a new tkinter window including basic setup
		"""

		# Main tkinter window
		self.root = tkinter.Tk()

		# Window Setup
		self.root.title("Text-Script")
		self.root.geometry("200x200")

		self.log.debug("Successfully created a new window.")

	def on_closing(self):
		"""
		Closes program if user clicks x button on the window
		"""

		self.log.debug("User clicked the window's x button. Exiting program.")

		self.root.destroy()


if __name__ == "__main__":

	# Initialize Logger
	L = Logger()

	L.log.debug("Program started from Gui.py.")

	# Initialize GUI
	g = Gui(L)

	# Close program if window is destroyed
	g.root.protocol("WM_DELETE_WINDOW", g.on_closing)

	# Tkinter mainloop
	L.log.debug("Starting Tkinter mainloop.")
	g.root.mainloop()
