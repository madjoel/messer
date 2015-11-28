# ----------------------
# Accepting thread class
# @author Matthieu Laqua
# ----------------------

# imports
import time, socket
import slog
from slog import dprint, lprint
from customthread import CustomThread

# thread that accepts connections
class AcceptThread(CustomThread):
    def __init__(self, sock, server):
        self.sock = sock
        self.parentServer = server
        CustomThread.__init__(self, description="AcceptThread")
    
    def run(self):
        self.sock.listen(3) # 3 as TEMP value
        while not self.shouldStop:
            try: conn, addr = self.sock.accept()
            except socket.timeout: continue
            lprint("<" + self.name + "> Incoming connection from:", addr)
            self.parentServer.addConnection((conn, addr))

        self.shutdownMsg()

