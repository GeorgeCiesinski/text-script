import tkinter
from Logger import Logger

class Gui:

	def __init__(self, log):

		# Instance wide log variable
		self.log = log.log

		self.create_window()

		#TODO: Create menu

	def create_window(self):

		"""
		create_window creates a new tkinter window including basic setup
		"""

		# Main tkinter window
		self.root = tkinter.Tk()

		# Window Setup
		self.root.title("Text-Script")
		self.root.geometry("400x400")


if __name__ == "__main__":

	# Initialize Logger
	L = Logger()

	L.log.debug("Program started from Gui.py.")

	# Initialize GUI
	g = Gui(L)

	# Tkinter mainloop
	g.root.mainloop()
