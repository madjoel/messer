# --------------------------
# UI class, contains windows
# @author Matthieu Laqua
# --------------------------

import time
from customthread import CustomThread
from threading import Lock
from screen import Screen

class UIThread(CustomThread):
    def __init__(self, client):
        self.parentClient = client
        self.screen = None
        self.msg_queue = []
        self.msg_queue_mutex = Lock()
        self.max_viewable_msgs = 10
        CustomThread.__init__(self, description="UIThread")

    def run(self):
        client = self.parentClient
        self.init()
        while not self.shouldStop:
            self.render_msgs()
            self.screen.refresh()
            time.sleep(1)

    def render_msgs(self):
        scr = self.screen
        if len(self.msg_queue) < self.max_viewable_msgs:
            msgs = self.msg_queue
        else:
            msgs = self.msg_queue[-(self.max_viewable_msgs):]
        for i in range(self.max_viewable_msgs):
            scr.clearln(i)
        for i in range(len(msgs)):
            scr.drawstr(0, i, msgs[i])

    def init(self):
        self.screen = Screen()

    def recv_msg(self, msg):
        self.msg_queue_mutex.acquire()
        self.msg_queue.append(msg)
        self.msg_queue_mutex.release()


    def print_err(self, errmsg):
        self.screen.clearln(10)
        self.screen.drawstr(0, 10, errmsg)
        self.screen.refresh()

