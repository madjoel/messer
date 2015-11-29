# ---------------------------------------
# Screen class using curses
# Wraps the terminal screen to a variable
# and displays everything on the screen
# @author Matthieu Laqua
# ---------------------------------------

# imports
import curses

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
        return self.screen.getch()

    # draws a string to the screen at the given coordinates
    def drawstr(self, x, y, s):
        self.screen.addstr(y, x, s)

    # clears the screen
    def clear(self):
        for y in range(self.height):
            for x in range(self.width):
                self.drawstr(x, y, " ")

    # refreshes the screen, makes changes visible
    def refresh(self):
        self.screen.refresh()

