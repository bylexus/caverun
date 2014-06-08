'''
C A V E R U N
==============
A fast-paced console cave runner

(c) 2014 alex@alexi.ch
    started as a hobby project to catch some python. Turned out to be funny, let's have
    a look where it leads to.

usage:
   Use your left/right arrow keys to move your caveman (bottom of screen), so that he
   does not collide with the walls.
'''

import curses
import sys
from game import Game



def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    game = Game(stdscr)
    return game.start()

try:
    duration = curses.wrapper(main)
    print("wat")
    print("\n\n You are D O O O O O M E D ! ! !\n\n")
    print("This time you lived %0.2f seconds.\n\n" % duration)
except KeyboardInterrupt:
    print("\nBah, you already give up? Pfff...\n")
    sys.exit(0)
