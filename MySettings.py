import configparser
import os.path

class MySettings:

	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config['DEFAULT'] = {
		'timer_in_seconds' : 180, 
		'pause_each_round_in_seconds' : 60, 
		'number_of_rounds' : 12,
		'notification_before_end_of_ring_in_seconds' : 10,
		'color_stop' : 'black',
		'color_run' : 'green',
		'color_pause' : 'red',
		'color_almost_end' : 'yellow',
		'logo' : 'logo.png'}
		self.filename = "boxing.ini"

	def loadFromFile(self):
		
		# If file not exist, write default value
		if not os.path.isfile(self.filename):
			self.saveToFile()

		# Load values
		self.config.read(self.filename)

	def saveToFile(self):
		with open(self.filename, 'w') as configfile:
			self.config.write(configfile)