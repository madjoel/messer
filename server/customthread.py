# ------------------------
# Base custom thread class
# @author Matthieu Laqua
# ------------------------

# imports
import time, threading
import slog
from slog import dprint, lprint

# custom thread
class CustomThread(threading.Thread):
	def __init__(self, description="CustomThread"): # constructor
		self.shouldStop = False # flag which can be set to shut down thread
		threading.Thread.__init__(self, name="CT-" + description)
	
	def run(self):
		while not self.shouldStop:
			time.sleep(1)
		self.shutdownMsg()
	
	def end(self):
		if not self.shouldStop:
			self.shouldStop = True
			self.shutdownAttemptMsg()
		else: self.alreadyShuttingDownMsg()
	
	def isShuttingDown(self):
		return self.shouldStop
	
	def shutdownAttemptMsg(self):
		dprint("<" + self.name + "> Attempting to shut down...")
	
	def alreadyShuttingDownMsg(self):
		dprint("<" + self.name + "> Thread is already shutting down...")

	def shutdownMsg(self):
		dprint("<" + self.name + "> Shut down.")

