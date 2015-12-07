# ---------------------------------------------
# Thread that communicates with a single client
# @author Matthieu Laqua
# ---------------------------------------------

# imports
import time, socket, threading
import slog
from slog import dprint, lprint
from customthread import CustomThread
from garbagethread import GarbageThread

# client thread class
class ClientThread(CustomThread):
    def __init__(self, ID, conn, server):
        self.ID = ID
        self.sock = conn[0]
        self.addr = conn[1]
        self.sock.settimeout(0.2)
        self.parentServer = server
        self.pendingMsgs = []
        self.msgLock = threading.Lock()
        CustomThread.__init__(self, description="ClientThread-" + str(self.ID))

    def run(self):
        while not self.shouldStop:
            self.msgLock.acquire()
            while len(self.pendingMsgs) > 0: # has pending messages
                self.sock.sendall(bytes(repr(self.pendingMsgs.pop(0)), "UTF-8"))
            self.msgLock.release()

            try: data = self.sock.recv(1024)
            except socket.timeout: continue
            except ConnectionResetError: break
            if not data: break
            else: #lprint("[Client " + str(self.ID) + "] " + str(data, "UTF-8"))
                message = str(data, "UTF-8").strip()
                self.parentServer.routeMessage(message, self.ID)
        
        self.sock.close()
        lprint("<" + self.name + "> Connection " + str(self.addr) + " closed.")
        GarbageThread(self.parentServer, self.ID).start()
        self.shutdownMsg()

    # sends a message to the client
    def send(self, message):
        self.msgLock.acquire()
        self.pendingMsgs.append(message)
        self.msgLock.release()

    def getAddr(self):
        return self.addr

    def getID(self):
        return self.ID

