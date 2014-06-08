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
import sys
if sys.version_info < (3,0):
    print("\n\n\nSorry. Too less python. Use python >= 3.0, please.\n\n\n")
    sys.exit(1);


import curses
from lib.game import Game

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    game = Game(stdscr)
    return game.start()




try:
    infos = curses.wrapper(main)
    print("\n\n You are D O O O O O M E D ! ! !\n\n")
    print("This time you lived {:0.2f} seconds".format(infos['survivalTime']))
    print("and collected {:d} pieces of gold!\n\n".format(infos['gold']))
except KeyboardInterrupt:
    print("\nBah, you already give up? Pfff...\n")
    sys.exit(0)
