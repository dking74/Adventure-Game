#######################################################
#
#	Creator : Devon King
#	Purpose : To create a program that plays a game
#
#	Course  : SWDV 600
#	Date    : 10/6
#   Notes   : This program contains dependencies...
#           : This will not work without them
#           : One dependency is pygame
#
#######################################################


from gameplay import Game
from display import MainDisplay
from music import Music
from thread import *
import time

def createGameandDisplay(themeSong):

    '''
    Purpose: createGameandDisplay
    Parameters: None
    
    Returns: Display and Game instances
    '''

    gameInstance = Game()
    displayInstance = MainDisplay()
    musicInstance = Music(themeSong)
    return gameInstance, displayInstance, musicInstance

def startThreads(displayInstance, gameInstance, musicInstance):

    '''
    Purpose: To create and start threads of execution
    Parameters:
        - displayInstance (MainDisplay): The display instance
        - gameInstance (Game): The game instance
    
    Returns: None
    '''

    musicThread = Thread("musicThread", 3, musicInstance.playThemeMusic, displayInstance)
    #displayThread = Thread("displayThread", 1, displayInstance.updateScene, gameInstance)
    # gameplayThread = Thread("playthread", 2, gameInstance.playGame, displayInstance)
    musicThread.startThread()
    # gameplayThread.startThread()
    # displayThread.startThread()

def main():

    gameInstance, \
    displayInstance, \
    musicInstance = createGameandDisplay('HarryPotterTheme.mp3')
    startThreads(gameInstance, displayInstance, musicInstance)
    displayInstance.getMouse()
    
if __name__ == "__main__":
    main()