# ------------------------
# Messer chat client class
# @author Matthieu Laqua
# ------------------------

# imports
import time, socket
from listenthread import ListenThread
from uithread import UIThread

class Client():
    def __init__(self, user, host, port):
        self.user = user
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10) # set to 10 to wait 10 secs for connection
        self.connect(self.addr)
        self.sock.settimeout(3)
        self.listen_thread = ListenThread(self)
        self.ui_thread = UIThread(self)

    def launch(self):
        self.ui_thread.start()
        self.listen_thread.start()

    def stop(self):
        self.listen_thread.end()
        self.ui_thread.end()

    def connect(self, addr):
        try:
            self.sock.connect(addr)
            print("Successfully connected.")
        except socket.timeout:
            print("Connection timed out.")
        except ConnectionRefusedError:
            print("Server not reachable.")
        time.sleep(1) # optional

    def recv_msg(self, msg):
        self.ui_thread.recv_msg(msg)

    def print_err(self, errmsg):
        self.ui_thread.print_err(errmsg)

