# ------------------------
# Messer chat client class
# @author Matthieu Laqua
# ------------------------

# imports
import time, socket
from listenthread import ListenThread
from ui import UI

class Client():
    def __init__(self, user, host, port):
        self.user = user
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(self.addr)
        self.listen_thread = ListenThread(self)
        self.ui = UI()

    def launch(self):
        ui = self.ui
        ui.init()
        self.listen_thread.start()

    def stop(self):
        self.listen_thread.end()

    def connect(self, addr):
        self.sock.settimeout(60)
        try: self.sock.connect(addr)
        except socket.timeout:
            print("Connection timed out.")
        except ConnectionRefusedError:
            print("Server not reachable.")
        self.sock.settimeout(3)
        print("Successfully connected.")
        time.sleep(1) # optional

    def recvMsg(self, msg):
        self.ui.appendMsg(msg)

    def printErr(self, errmsg):
        self.ui.errorMsg(errmsg)

