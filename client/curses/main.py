#!/bin/python
# -------------------------
# Messer chat curses client
# main/entrypoint
# @author Matthieu Laqua
# -------------------------

# imports
import sys
from client import Client

# main function
def main():
    # default values for login
    user = "nameless"
    host = "localhost"
    port = 13370

    # parse arguments
    for arg in sys.argv:
        if arg.startswith("-u="):
            user = arg[3:]
        elif arg.startswith("-h="):
            host = arg[3:]
        elif arg.startswith("-p="):
            try: port = int(arg[3:])
            except ValueError:
                print("Invalid port: " + arg[3:])
                return

    # start the client
    client = Client(user, host, port)
    client.launch()

# entrypoint
if __name__ == "__main__":
    # launch main function
    main()

