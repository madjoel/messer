#!/usr/bin/python3

# ----------------------
# "Messer" chat server
# @author Matthieu Laqua
# ----------------------

# imports
import sys, time, socket, re
import slog
from slog import dprint, lprint
from server import *

# main function
def main():
    port = 13370 # default port
    for arg in sys.argv:
        if arg == "-d":
            slog.DEBUG = True
        elif arg.startswith("-p="):
            try: port = int(arg[3:])
            except ValueError: lprint("Invalid port: " + arg[3:], mtype=1)
        elif arg in ["-h", "-help", "-?"]:
            print("Arguments:" +
                    "\n -d       :show debug messages" +
                    "\n -p=<int> :set port number" +
                    "\n -h       :show this help")
            return

    socket.setdefaulttimeout(3) # set default timeout of all sockets
    server = Server(port) # bind to port
    server.serve() # start listening
    while not server.stopped:
        try: time.sleep(1)
        except KeyboardInterrupt:
            lprint("Received keyboard interrupt signal; use command 'stop' to quit instead.")
            break
        if slog.DEBUG: break

# defines entrypoint
if __name__ == "__main__":
    main()

