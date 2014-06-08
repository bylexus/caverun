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
    gold = 0

    screen = []

    def __init__(self,scr):
        self.scr = scr
        self.height, self.width = self.scr.getmaxyx()
        self.width = self.width -1
        self.gapWidth = 40
        self.gapPos = int(self.width / 2 - self.gapWidth / 2)
        self.playerPos = int(self.width / 2)

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_RED)

        for i in range(0,self.height):
            self.screen.append(" "*self.width)

    def getNextLine(self):
        self.gapPos = min(self.width-self.gapWidth,max(0,self.gapPos + random.randint(-1*self.gapMove,self.gapMove)))
        line = list(self.gapPos * "#" + self.gapWidth*" " + (self.width - (self.gapPos+self.gapWidth))*"#")
        self.addSomeGold(line)
        if len(line) > self.width:
            line = line[:self.width]
        return line

    def addSomeGold(self,line):
        if random.randint(0,10) == 5:
            pos = random.randint(self.gapPos,self.gapPos+self.gapWidth)
            line[pos] = 'g'
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
        self.scr.addstr(0,0,"  Speed: {:0.2f} ".format(1 / self.delay))

    def drawTime(self):
        # add time display:
        timeStr = "  {:0.2f}s  ".format(time.time()-self.startTime)
        self.scr.addstr(0,self.width-len(timeStr)-2,timeStr)

    def drawWorld(self):
        for y,line in enumerate(self.getNextScreen()):
            for x,char in enumerate(line):
                if char == 'g':
                    self.scr.addstr(y,x,'G',curses.color_pair(2) | curses.A_BOLD)
                else:
                    self.scr.addstr(y,x,char)

    def drawPlayer(self):
        # add player:
        self.scr.addstr(self.height-1,self.playerPos,'@',curses.color_pair(1) | curses.A_BOLD)

    def collectGold(self):
        bottomLine = self.screen[0]
        if 'g' in bottomLine[self.playerPos-1:self.playerPos+1]:
            self.gold += 1

    def drawGoldPointer(self):
        goldStr = "  {:05d}  ".format(self.gold)
        self.scr.addstr(1,self.width-len(goldStr)-2,goldStr,curses.color_pair(2) | curses.A_BOLD)

    def updateScreen(self):
        self.drawWorld()
        self.drawTime()
        self.drawSpeed()
        self.drawPlayer()
        self.collectGold()
        self.drawGoldPointer()
        self.scr.refresh()
