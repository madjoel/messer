# ------------------------
# Input handler for curses
# @author Matthieu Laqua
# ------------------------

from customthread import CustomThread

class UIInputThread(CustomThread):
    def __init__(self, ui_thread):
        self.ui_thread = ui_thread
        CustomThread.__init__(self, description="UIInputThread")

