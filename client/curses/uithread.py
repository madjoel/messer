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
        self.cmd_line_nr = 13 # "
        self.cmd_line_len = 80 # "
        self.cmd_cursor_pos = 0 # @ beginning of cmd line
        self.ui_input_thread = None
        CustomThread.__init__(self, description="UIThread")

    def init(self):
        self.screen = Screen()
        self.update_dimension()
        self.ui_input_thread = UIInputThread(self, self.screen)

    def update_dimension(self):
        scr = self.screen
        self.max_viewable_msgs  = scr.height - 4 # may be changed
        self.cmd_line_nr        = scr.height - 1 # display in last line
        self.cmd_line_len       = scr.width  - 3 # because of "> " and cursor

    def run(self):
        self.init()
        self.ui_input_thread.start()
        self.render_cmdline() # render once
        while not self.shouldStop:
            self.render_msgs()
            time.sleep(0.3)

    def render_msgs(self):
        scr = self.screen
        oldx, oldy = scr.get_cursor_pos()
        self.msg_queue_mutex.acquire()
        if len(self.msg_queue) <= self.max_viewable_msgs:
            msgs = self.msg_queue[:] # slice it to make a copy
        else:
            msgs = self.msg_queue[-(self.max_viewable_msgs):]
        self.msg_queue_mutex.release()
        for i in range(self.max_viewable_msgs):
            scr.clearln(i)
        for i in range(len(msgs)):
            scr.drawstr(0, i, msgs[i])
        scr.set_cursor_pos(oldx, oldy)
        scr.refresh()

    def render_cmdline(self):
        scr = self.screen
        cmdline = self.ui_input_thread.get_buffer()
        scr.clearln(self.cmd_line_nr)
        scr.drawstr(0, self.cmd_line_nr, "> " + cmdline[-80:])
        scr.set_cursor_pos(2 + len(cmdline[-80:]), self.cmd_line_nr)
        scr.refresh()

    def handle_command(self, cmd):
        client = self.parent_client
        if len(cmd) == 0: # just pressed return
            return
        if not cmd.startswith("/"):
            client.send_msg(cmd)
            self.append_msg("<-- " + cmd)
        else: # is a command
            if cmd[1:].lower() == "stop":
                client.stop()
            if cmd[1:].lower() == "clear":
                self.clear_msg_queue()

    def clear_msg_queue(self):
        self.msg_queue_mutex.acquire()
        self.msg_queue = list()
        self.msg_queue_mutex.release()

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

