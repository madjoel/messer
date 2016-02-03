# ------------------------
# Input handler for curses
# @author Matthieu Laqua
# ------------------------

import time, curses
from customthread import CustomThread

class UIInputThread(CustomThread):
    def __init__(self, uithread, screen):
        self.parent_uithread = uithread
        self.screen = screen
        self.visible_buffer = "<cmd line>" # for debugging
        CustomThread.__init__(self, description="UIInputThread")
        self.daemon = True

    def run(self):
        scr = self.screen
        while not self.shouldStop:
            key = scr.get_key_pressed()
            self.handle_key(key)
            self.parent_uithread.render_cmdline()

    def handle_key(self, key):
        #visbuf = self.visible_buffer
        #if (key == curses.KEY_BACKSPACE):
        #    visbuf = visbuf[:-1]
        #else:
        #    visbuf += chr(key)
        self.visible_buffer
        if (key == curses.KEY_BACKSPACE):
            self.visible_buffer = self.visible_buffer[:-1]
        else:
            self.visible_buffer += chr(key)

    def get_buffer(self):
        return self.visible_buffer

