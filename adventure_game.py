from gameplay import Game
from display import *
from thread import *

def main():
    displayThread = Thread("displayThread", 1, Display.updateScene())
    gameplayThread = Thread("playthread", 2, Game.playGame())
    gameplayThread.startThread()
    displayThread.startThread()
    
if __name__ == "__main__":
    main()