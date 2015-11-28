# -----------------------
# Client managing Thread
# @author Matthieu Laqua
# -----------------------

# imports
import time, threading
import slog
from slog import dprint, lprint
from customthread import CustomThread
from message import Message

# Thread that manages all messages, that neet to be send
class ManageThread(CustomThread):
	def __init__(self, server):
		self.parentServer = server
		self.msgLock = threading.Lock()
		self.msgQueue = []
		CustomThread.__init__(self, description="ManageThread")
	
	def run(self):
		while not self.shouldStop:
			self.msgLock.acquire()
			if len(self.msgQueue) > 0:
				message = self.msgQueue.pop(0)
				dprint("<" + self.name + "> " + repr(message))
				if message.text.startswith("[cur]"):
					new_username = message.text[5:]
					dprint("<" + self.name + "> Client " + str(message.sender_id)
						 + " wants to be called: '" + new_username + "'")
					if self.parentServer.usernameExists(new_username):
						self.parentServer.sendToClient("[cun]" + new_username
													 + " exists", message.sender_id)
						dprint("<" + self.name + "> New username '" + new_username + "' exists")
					else:
						self.parentServer.renameClient(new_username, message.sender_id)
						self.parentServer.sendToClient("[cua]" + new_username, message.sender_id)
						dprint("<" + self.name + "> New username '" + new_username + "' was set")
			self.msgLock.release()
			time.sleep(0.2)
		self.shutdownMsg()
	
	def addToQueue(self, message, sender_id):
		self.msgLock.acquire()
		dprint("<" + self.name + "> " + str(sender_id) + " sent '" + message + "'")
		self.msgQueue.append(Message(message, [], sender_id, self.parentServer.getUsername(sender_id)))
		self.msgLock.release()

