# ---------------------------------------
# Screen class using curses
# Wraps the terminal screen to a variable
# and displays everything on the screen
# @author Matthieu Laqua
# ---------------------------------------

# imports
import curses, threading

# class definition
class Screen:
    # constructor
    def __init__(self):
        self.screen = curses.initscr() # wrap the terminal screen
        curses.noecho() # dont echo typed keys
        curses.cbreak() # react to keys instantly
        self.screen.keypad(True) # handle keys
        #self.screen.nodelay(True) # dont wait for the user to input text
        #curses.curs_set(False) # hide cursor

        self.width  = curses.COLS
        self.height = curses.LINES
        self.lock = threading.Lock()

    # destructor
    def __del__(self):
        # make sure that the screen gets restored properly
        # even when just the object is destroyed
        #self.restore() # deactivated for debugging
        pass

    # restore the terminal screen
    def restore(self):
        # revert settings
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.curs_set(True)
        curses.endwin()

    # wraps the scr.getch()
    def get_key_pressed(self):
        char = self.screen.getch()
        if char == curses.KEY_RESIZE:
            curses.update_lines_cols()
            self.width  = curses.COLS
            self.height = curses.LINES
        return char

    # push one char so that getch() will return it
    def push_char(self, char):
        curses.ungetch(char)

    # draws a string to the screen at the given coordinates
    def drawstr(self, x, y, s):
        self.lock.acquire()
        self.screen.insstr(y, x, s)
        self.lock.release()

    # clears the screen
    def clear(self):
        for y in range(self.height):
            for x in range(self.width):
                self.drawstr(x, y, " ")

    # clears one line
    def clearln(self, line):
        self.lock.acquire()
        for x in range(self.width):
            self.screen.insstr(line, x, " ")
        self.lock.release()

    # returns the cursor pos (x, y)
    def get_cursor_pos(self):
        y, x = curses.getsyx()
        return (x, y) # rotate the tuple to fit (x, y)

    # sets the cursor pos
    def set_cursor_pos(self, x, y):
        self.lock.acquire()
        curses.setsyx(y, x)
        self.screen.move(y, x)
        self.lock.release()

    # refreshes the screen, makes changes visible
    def refresh(self):
        self.lock.acquire()
        self.screen.refresh()
        self.lock.release()

