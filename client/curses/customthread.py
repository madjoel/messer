# ------------------------
# Base custom thread class
# @author Matthieu Laqua
# ------------------------

# imports
import time, threading

# custom thread
class CustomThread(threading.Thread):
    def __init__(self, description="CustomThread"): # constructor
        self.shouldStop = False # flag which can be set to shut down thread
        threading.Thread.__init__(self, name="CT-" + description)

    def run(self):
        while not self.shouldStop:
            time.sleep(1)
        self.shutdownAction()

    def end(self):
        if not self.shouldStop:
            self.shouldStop = True
            self.shutdownAttemptAction()
        else: self.alreadyShuttingDownAction()

    def isShuttingDown(self):
        return self.shouldStop

    def shutdownAttemptAction(self): pass

    def alreadyShuttingDownAction(self): pass

    def shutdownAction(self): pass

