# -----------------------------
# Thread that wraps the console
# @author Matthieu Laqua
# -----------------------------

# imports
import time, sys, re
import slog
from slog import dprint, lprint
from customthread import CustomThread
from message import Message

# thread that controls the console
class ConsoleThread(CustomThread):
    def __init__(self, server):
        self.parentServer = server
        CustomThread.__init__(self, description="ConsoleThread")
    
    def run(self):
        while not self.shouldStop:
            stdinput = sys.stdin.readline() # blocking call
            command = stdinput.strip()
            if command != "":
                dprint("<Console> Echoing input: " + command)
            if command.lower() in ["h", "help", "?"]:
                lprint("<Console> Available commands: stop/q, ls/list, kickid, " +
                       "broadcast, send..to")
            elif command.lower() in ["stop", "q"]:
                self.parentServer.stop()
                break
            elif command.lower() in ["ls", "list"]:
                self.parentServer.ls()
            elif command.lower().startswith("kickid "):
                try: cid = int(command[7:].strip())
                except ValueError:
                    lprint("Invalid id for kickid command: '" + cid + "'")
                    continue
                if cid in self.parentServer.connections:
                    self.parentServer.closeConnection(cid)
                else: lprint("<Console> ID '" + str(cid) + "' is not present on this server.", mtype=1)
            elif command.lower().startswith("broadcast "):
                message = command[10:]
                self.parentServer.broadcast("[Server] " + message)
                lprint("<Console> Broadcast done.")
            elif re.search('send .+ to ', command):
                message = re.search("send .* to", command).group().replace("send ", "", 1).replace(" to", "", 1)
                recipient = re.search('to .*', command).group().replace("to ", "", 1)
                dprint("<Console> message='" + message + "', recipient='" + recipient + "'")
                try:
                    recipient = int(recipient)
                    self.parentServer.sendToClient("[Server] " + message, recipient)
                    lprint("<Console> Message sent to client.")
                except ValueError: lprint("<Console> Invalid recipient.")
            else:
                lprint("Don't know what to do with: '" + command + "'", mtype=3)
        self.shutdownMsg()

