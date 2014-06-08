import time
import curses
from world import World

class Game:
    scr = None
    world = None
    def __init__(self, scr):
        self.scr = scr

    def start(self):
        self.world = World(self.scr)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLUE)
        return self.gameLoop()

    def gameLoop(self):
        startTime = time.time()
        levelTimeCount = 0
        self.world.startTime = startTime
        while True:
            loopStart = time.time()
            if levelTimeCount > 10:
                self.world.increaseLevel()
                levelTimeCount = 0

            key = self.scr.getch()
            if key in [curses.KEY_LEFT,ord('a'),ord('h')]:
                self.world.movePlayerLeft()
            if key in [curses.KEY_RIGHT,ord('d'),ord('l')]:
                self.world.movePlayerRight()

            self.world.updateScreen()

            
            if self.world.playerIsDead():
                return time.time() - startTime
            loopDuration = time.time()-loopStart
            levelTimeCount += self.world.delay
            time.sleep(self.world.delay - loopDuration)
