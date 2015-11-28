# ----------------------
# Small logging module
# @author Matthieu Laqua
# ----------------------

# imports
import time
from enum import Enum

# global variables
DEBUG = False

# enum of message types
class Flags(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    WTF = 3

# log a line prefixed with date and time
def lprint(*message, mtype=-1):
    print(time.strftime("[%d.%m.%y %H:%M:%S]"), end=" ")
    if mtype != -1:
        print("[" + Flags(mtype).name + "]", end=" ")
    for m in message:
        print(m, end=" ")
    print(flush=True)

# only print a line when debug mode is active
def dprint(*message):
    if DEBUG:
        print(time.strftime("[%d.%m.%y %H:%M:%S]") + " [Debug]", end=" ")
        for m in message:
            print(m, end=" ")
        print(flush=True)
