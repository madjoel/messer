# ------------------------
# Messer chat client class
# @author Matthieu Laqua
# ------------------------

# imports
import time, socket
from screen import Screen
from listenthread import ListenThread
from window import Window

class Client():
    def __init__(self, user, host, port):
        self.user = user
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(self.addr)
        self.listen_thread = ListenThread(self)
        self.window = Window()

    def launch(self):
        win = self.window
        win.init()
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
        self.window.appendMsg(msg)

    def printErr(self, errmsg):
        self.window.errorMsg(errmsg)

