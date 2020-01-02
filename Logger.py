import logging
from logging import handlers
from os import path


class Logger:

	def __init__(self):
		"""
		Initializes an instance of Logging and configures the instance
		"""

		# Basic Settings
		self.log = logging.getLogger(__name__)
		self.log.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')

		# Check if logs exist
		self.rollover_check = path.exists('Logs/logs.log')

		# Rotating File Handler (5 backups)
		self.file_handler = handlers.RotatingFileHandler('Logs/logs.log', mode='w', maxBytes=10000, backupCount=5)
		self.file_handler.setFormatter(formatter)
		self.log.addHandler(self.file_handler)

		# Perform rollover check
		self.roll_over()

	def roll_over(self):
		"""
		If log exists, rollover
		"""

		if self.rollover_check:
			self.file_handler.doRollover()
