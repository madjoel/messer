# -------------------------------------
# Grabage thread, cleans up connections
# @author Matthieu Laqua
# -------------------------------------

# imports
import time
import slog
from slog import dprint, lprint
from customthread import CustomThread

# thread that accepts connections
class GarbageThread(CustomThread):
	def __init__(self, server, client_id):
		self.parentServer = server
		self.client_id = client_id
		CustomThread.__init__(self, description="GarbageThread-" + str(self.client_id))
	
	def run(self):
		self.parentServer.closeConnection(self.client_id)
		self.shutdownMsg()

