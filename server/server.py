# --------------------------------------
# Module which contains the server class
# @author Matthieu Laqua
# --------------------------------------

# imports
import sys, socket, threading
import slog
from slog import dprint, lprint
from acceptthread import *
from consolethread import *
from clientthread import *
from msgcenterthread import *
from managethread import *
from message import Message

# server class
class Server:
    def __init__(self, port):
        self.stopped = False
        self.host = ""
        self.port = port
        #
        self.users = dict()
        self.userLock = threading.Lock()
        self.connections = dict()
        self.conLock = threading.Lock()
        #
        for i in range(180): # try 3 minutes to bind the socket
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind((self.host, self.port)) # bind socket to localhost:port
                dprint("Port is set to: " + str(self.port))
                dprint("Address bound successfully.")
                break
            except OSError:
                if i == 0: lprint("Address not available yet, waiting...")
                self.sock.close()
                print("\rTime passed: " + str(i+1) + "s", end="", flush=True)
                time.sleep(1)
        else:
            sys.exit(2) # could not bind to address
        #
        self.msgcenter_thread = MSGCenterThread(self)
        self.manage_thread = ManageThread(self)
        self.accept_thread = AcceptThread(self.sock, self)
        self.console_thread = ConsoleThread(self)
        lprint("Server started successfully on port " + str(self.port))

    def __del__(self):
        self.sock.close()

    # starts the server
    def serve(self):
        self.accept_thread.start()
        self.console_thread.start()
        self.msgcenter_thread.start()
        self.manage_thread.start()

    # shuts down the server
    def stop(self):
        lprint("Shutting down server...")
        self.msgcenter_thread.end()
        self.manage_thread.end()
        self.console_thread.end()
        self.accept_thread.end()
        self.accept_thread.join()
        self.msgcenter_thread.join()
        self.manage_thread.join()
        self.closeAllConnections()
        #self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.stopped = True

    # lists all connections established
    def ls(self):
        self.conLock.acquire()
        if len(self.connections) > 0:
            lprint("Listing all Connections:")
            self.userLock.acquire()
            for client_id in self.connections:
                lprint("ID " + str(self.connections[client_id].getID()) + ": "
                        + str(self.connections[client_id].getAddr()) + " "
                        + "'" + self.users[client_id] + "'")
            self.userLock.release()
        else: lprint("No connections established.")
        self.conLock.release()

    # returns all ids in self.connections
    def getIDs(self):
        self.conLock.acquire()
        ids = list(self.connections.keys())
        self.conLock.release()
        return ids

    # returns the next available ID
    def nextID(self):
        ids = self.getIDs()
        i = 1
        while i in ids:
            i += 1
        return i

    # adds a connection to the list
    def addConnection(self, conn):
        newID = self.nextID()
        self.conLock.acquire()
        self.connections[newID] = ClientThread(newID, conn, self)
        self.connections[newID].start()
        self.connections[newID].send("Welcome client no. " + str(newID))
        self.conLock.release()
        self.userLock.acquire()
        self.users[newID] = "nameless"
        self.userLock.release()

    # closes a connection and removes it from the list
    def closeConnection(self, client_id):
        self.conLock.acquire()
        if client_id in self.connections:
            self.connections[client_id].end()
            self.connections[client_id].join()
            del self.connections[client_id]
            self.userLock.acquire()
            del self.users[client_id]
            self.userLock.release()
        self.conLock.release()

    # closes all connections which are established
    def closeAllConnections(self):
        self.conLock.acquire()
        client_ids = list(self.connections.keys())
        for client_id in client_ids:
            self.connections[client_id].end()
            self.connections[client_id].join()
            del self.connections[client_id]
        self.conLock.release()

    # send a single message to a single client
    def sendToClient(self, message, client_id):
        self.conLock.acquire()
        self.connections[client_id].send(message)
        self.conLock.release()

    # gets the username of a client
    def getUsername(self, client_id):
        self.userLock.acquire()
        if client_id in self.users:
            username = self.users[client_id]
        else:
            username = "nameless"
        self.userLock.release()
        return username

    # checks if username exists
    def usernameExists(self, username):
        self.userLock.acquire()
        namelist = list(self.users.values())
        self.userLock.release()
        if username in namelist:
            return True
        else:
            return False

    # rename a client
    def renameClient(self, new_username, client_id):
        self.userLock.acquire()
        self.users[client_id] = new_username
        self.userLock.release()

    # broadcast a message to all clients
    def broadcast(self, message):
        self.conLock.acquire()
        for ct in self.connections.values():
            ct.send(message)
        self.conLock.release()

    # routes a message to the specified clients
    def routeMessage(self, message, sender_id):
        if not message.startswith("["):
            self.msgcenter_thread.addToQueue(message, sender_id)
        else:
            self.manage_thread.addToQueue(message, sender_id)

