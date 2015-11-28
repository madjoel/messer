# -----------------------
# Message managing Thread
# @author Matthieu Laqua
# -----------------------

# imports
import time, threading
import slog
from slog import dprint, lprint
from customthread import CustomThread
from message import Message

# Thread that manages all messages, that neet to be send
class MSGCenterThread(CustomThread):
	def __init__(self, server):
		self.parentServer = server
		self.msgLock = threading.Lock()
		self.msgQueue = []
		CustomThread.__init__(self, description="MSGCenterThread")
	
	def run(self):
		while not self.shouldStop:
			self.msgLock.acquire()
			if len(self.msgQueue) > 0:
				message = self.msgQueue.pop(0)
				while message.hasRecipient():
					self.parentServer.sendToClient(message, message.nextRecipient())
			self.msgLock.release()
			time.sleep(0.1)
		self.shutdownMsg()
	
	def addToQueue(self, message, sender_id):
		self.msgLock.acquire()
		ids = self.parentServer.getIDs()
		if sender_id in ids:
			ids.remove(sender_id)
		dprint("<" + self.name + "> " + str(sender_id) + " sent '" + message + "' to " + str(ids))
		self.msgQueue.append(Message(message, ids, sender_id, self.parentServer.getUsername(sender_id)))
		self.msgLock.release()

