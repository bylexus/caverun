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
import random
import time
import curses
import sys

class World:
    width = 0
    heigth = 0

    gapWidth = 0
    gapPos = 0
    gapMove = 2

    playerPos = 0
    playerSpeed = 2

    delay = 0.03

    screen = []

    def __init__(self,width,height):
        self.width = width -1
        self.height = height
        self.gapWidth = 40
        self.gapPos = self.width / 2 - self.gapWidth / 2
        self.playerPos = self.width / 2
        for i in range(0,self.height):
            self.screen.append(" "*self.width)

    def getNextLine(self):
        line = self.width * "#"
        self.gapPos = min(self.width-self.gapWidth,max(0,self.gapPos + random.randint(-1*self.gapMove,self.gapMove)))
        line = self.gapPos * "#" + self.gapWidth*" " + (self.width - (self.gapPos+self.gapWidth))*"#"
        if len(line) > self.width:
            line = "".join(list(line)[:self.width])
        return line

    def getNextScreen(self):
        self.screen.append(self.getNextLine())
        self.screen = self.screen[1:]
        return reversed(self.screen)

    def movePlayerLeft(self):
        self.playerPos = max(0,self.playerPos - self.playerSpeed)

    def movePlayerRight(self):
        self.playerPos = min(self.width,self.playerPos + self.playerSpeed)

    def playerIsDead(self):
        bottomLine = self.screen[0]
        return bottomLine[self.playerPos] == "#"

    def increaseSpeed(self):
        self.delay = max(0.002,self.delay * 0.8)

    def increaseWobblyness(self):
        self.gapMove = min(self.width / 2,self.gapMove + 1)

    def increaseLevel(self):
        self.increaseSpeed()
        self.increaseWobblyness()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    h,w = stdscr.getmaxyx()
    wb = World(w,h)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLUE)
    startTime = time.time()
    levelTimeCount = 0
    while True:
        loopStart = time.time()
        if levelTimeCount > 10:
            wb.increaseLevel()
            levelTimeCount = 0

        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            wb.movePlayerLeft()
        if key == curses.KEY_RIGHT:
            wb.movePlayerRight()

        for y,line in enumerate(wb.getNextScreen()):
            stdscr.addstr(y,0,line)

        # add speed info:
        stdscr.addstr(0,0,"  Speed: %0.2f " % (1 / wb.delay))

        # add time display:
        timeStr = "  %0.2fs  " % (time.time() - startTime)
        stdscr.addstr(0,w-len(timeStr)-2,timeStr)

        # add player:
        stdscr.addstr(h-1,wb.playerPos,'@',curses.color_pair(1) | curses.A_BOLD)
        stdscr.refresh()
        if wb.playerIsDead():
            return time.time() - startTime
        loopDuration = time.time()-loopStart
        levelTimeCount += wb.delay
        time.sleep(wb.delay - loopDuration)

try:
    duration = curses.wrapper(main)
    print "\n\n You are D O O O O O M E D ! ! !\n\n"
    print "This time you lived %0.2f seconds.\n\n" % duration
except KeyboardInterrupt:
    print "\nBah, you already give up? Pfff...\n"
    sys.exit(0)
