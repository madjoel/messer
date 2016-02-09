# ----------------------------------------------
# UIThread class: renders UI an handles commands
# @author Matthieu Laqua
# ----------------------------------------------

import time
from customthread import CustomThread
from threading import Lock
from screen import Screen
from uiinputthread import UIInputThread
from message import Message

class UIThread(CustomThread):
    def __init__(self, client):
        self.parent_client = client
        self.screen = None
        self.msg_queue = []
        self.msg_queue_mutex = Lock()
        self.max_viewable_msgs = 10 # will be adjusted
        self.ui_input_thread = None
        CustomThread.__init__(self, description="UIThread")

    def init(self):
        self.screen = Screen()
        self.ui_input_thread = UIInputThread(self, self.screen)

    def run(self):
        self.init()
        self.ui_input_thread.start()
        while not self.shouldStop:
            self.render_msgs()
            time.sleep(0.3)

    def render_msgs(self):
        scr = self.screen
        oldx, oldy = scr.get_cursor_pos()
        if len(self.msg_queue) < self.max_viewable_msgs:
            msgs = self.msg_queue
        else:
            msgs = self.msg_queue[-(self.max_viewable_msgs):]
        for i in range(self.max_viewable_msgs):
            scr.clearln(i)
        for i in range(len(msgs)):
            scr.drawstr(0, i, msgs[i])
        scr.set_cursor_pos(oldx, oldy)
        scr.refresh()

    def render_cmdline(self):
        cmd_line_nr = 13 # for debugging
        cmd_line_len = 80
        scr = self.screen
        cmdline = self.ui_input_thread.get_buffer()
        scr.clearln(cmd_line_nr)
        scr.drawstr(0, cmd_line_nr, "> " + cmdline[-80:])
        scr.refresh()

    def handle_command(self, cmd):
        client = self.parent_client
        if not cmd.startswith("/"):
            client.send_msg(cmd)
            self.append_msg("<-- " + cmd)
        else: # is a command
            if cmd[1:].lower() == "stop":
                client.stop()

    def append_msg(self, msg):
        self.msg_queue_mutex.acquire()
        self.msg_queue.append(msg)
        self.msg_queue_mutex.release()

    def recv_msg(self, msg):
        msg = Message.fromstring(msg, [])
        self.append_msg("--> " + msg.sender_name + ": " + msg.text)

    def print_err(self, errmsg):
        self.screen.clearln(self.max_viewable_msgs)
        self.screen.drawstr(0, self.max_viewable_msgs, "*** " + errmsg)
        self.screen.refresh()

