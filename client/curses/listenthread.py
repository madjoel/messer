# ----------------------------------------------
# Thread that listens on the provided connection
# @author Matthieu Laqua
# ----------------------------------------------

import socket
from customthread import CustomThread

# thread for listening
class ListenThread(CustomThread):
    def __init__(self, client):
        self.parentClient = client
        CustomThread.__init__(self, description="ListenThread")

    def run(self):
        client = self.parentClient
        while not self.shouldStop:
            try: data = client.sock.recv(1024)
            except socket.timeout: continue
            if not data:
                client.print_err("Connection closed.")
                break # stop listen thread
            else:
                client.recv_msg(str(data, "UTF-8"))

