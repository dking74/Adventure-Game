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
from thread import Thread

class WindowClosed(Exception):
    """Exception raised when screen is no longer active"""
    pass

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

def continueForever(display):
    
    """Keep reading forever,
       until the screen is no longer active"""
    while True:
        try:
            mouse = display.getMouse()
        except Exception:
            import sys
            sys.exit()

def startThreads(gameInstance, displayInstance, musicInstance):

    '''
    Purpose: To create and start threads of execution
    Parameters:
        - displayInstance (MainDisplay): The display instance
        - gameInstance (Game): The game instance
        - musicInstance (Music): The music player
    
    Returns: None
    '''

    musicThread = Thread("musicThread", 3, musicInstance.playThemeMusic, displayInstance)
    gameplayThread = Thread("playthread", 2, gameInstance.playGame, displayInstance)
    displayInstance.updateScene(gameInstance)
    continueForever(displayInstance)

def main():

    # initialize game
    gameInstance, \
    displayInstance, \
    musicInstance = createGameandDisplay('HarryPotterTheme.mp3')

    # start worker threads --> main gui thread has to run in main loop
    startThreads(gameInstance, displayInstance, musicInstance)
    
if __name__ == "__main__":
    main()