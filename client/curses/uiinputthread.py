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
        if (key == curses.KEY_BACKSPACE):
            self.visible_buffer = self.visible_buffer[:-1]
        elif (key == ord('\t')):
            self.visible_buffer += "    " # convert tab to 4 spaces
        elif (key == curses.KEY_ENTER or key == 10):
            self.parent_uithread.handle_command(self.visible_buffer)
            self.visible_buffer = ""
        else:
            self.visible_buffer += chr(key)

    def get_buffer(self):
        return self.visible_buffer

