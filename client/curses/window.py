# ------------------------
# Rudimentary window class
# @author Matthieu Laqua
# ------------------------

from screen import Screen

class Window:
    def __init__(self):
        self.screen = None

    def init(self):
        self.screen = Screen()

    def appendMsg(self, msg):
        self.screen.clearln(0)
        self.screen.drawstr(0, 0, msg)
        self.screen.refresh()

    def errorMsg(self, errmsg):
        self.screen.clearln(1)
        self.screen.drawstr(0, 1, errmsg)
        self.screen.refresh()

