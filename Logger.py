import logging
from logging import handlers
from os import path
import glib


class Logger:

	def __init__(self):
		"""
		Initializes an instance of Logging and configures the instance
		"""

		# Logs directory
		self.log_dir = "Logs/"

		# Basic Settings
		self.log = logging.getLogger(__name__)
		self.log.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')

		# Create directory if doesn't exist
		if not glib.check_directory(self.log_dir):
			glib.create_folder(self.log_dir)
			print("Created Logs directory as it did not exist.")

		# Check if logs exist
		self._rollover_check = path.exists('Logs/logs.log')

		# Rotating File Handler (5 backups)
		self._file_handler = handlers.RotatingFileHandler('Logs/logs.log', mode='w', maxBytes=10000, backupCount=5)
		self._file_handler.setFormatter(formatter)
		self.log.addHandler(self._file_handler)

		# Perform rollover check
		self._roll_over()

	def _roll_over(self):
		"""
		If log exists, rollover
		"""

		if self._rollover_check:
			self._file_handler.doRollover()
