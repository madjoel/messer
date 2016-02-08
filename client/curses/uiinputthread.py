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
        self.visible_buffer = ""
        CustomThread.__init__(self, description="UIInputThread")
        self.daemon = True

    def run(self):
        uithread = self.parent_uithread
        scr = self.screen
        uithread.render_cmdline() # render once
        while not self.shouldStop:
            key = scr.get_key_pressed()
            self.handle_key(key)
            uithread.render_cmdline()

    def handle_key(self, key):
        uithread = self.parent_uithread
        if (key == curses.KEY_BACKSPACE):
            self.visible_buffer = self.visible_buffer[:-1]
        elif (key == ord('\t')):
            self.visible_buffer += "    " # convert tab to 4 spaces
        elif (key == curses.KEY_ENTER or key == 10):
            token = self.visible_buffer
            self.visible_buffer = ""
            uithread.render_cmdline()
            uithread.handle_command(token)
        else:
            self.visible_buffer += chr(key)

    def get_buffer(self):
        return self.visible_buffer

