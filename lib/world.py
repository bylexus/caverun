import random
import curses
import time

class World:
    scr = None
    width = 0
    heigth = 0

    gapWidth = 0
    gapPos = 0
    gapMove = 2

    playerPos = 0
    playerSpeed = 2

    delay = 0.03

    startTime = 0

    screen = []

    def __init__(self,scr):
        self.scr = scr
        self.height, self.width = self.scr.getmaxyx()
        self.width = self.width -1
        self.gapWidth = 40
        self.gapPos = int(self.width / 2 - self.gapWidth / 2)
        self.playerPos = int(self.width / 2)
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

    def drawSpeed(self):
        # add speed info:
        self.scr.addstr(0,0,"  Speed: %0.2f " % (1 / self.delay))

    def drawTime(self):
        # add time display:
        timeStr = "  %0.2fs  " % (time.time()-self.startTime)
        self.scr.addstr(0,self.width-len(timeStr)-2,timeStr)

    def drawWorld(self):
        for y,line in enumerate(self.getNextScreen()):
            self.scr.addstr(y,0,line)

    def drawPlayer(self):
        # add player:
        self.scr.addstr(self.height-1,self.playerPos,'@',curses.color_pair(1) | curses.A_BOLD)
        

    def updateScreen(self):
        self.drawWorld()
        self.drawTime()
        self.drawSpeed()
        self.drawPlayer()
        self.scr.refresh()
