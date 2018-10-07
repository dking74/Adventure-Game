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
from thread import *

def installPyGame():
          
    """Function to install Pygame if not already installed"""
    try:
        import pygame
    except ImportError:
        try:    
            import os
            os.system('python3 -m pip install -U pygame --user')
        except Exception:
            return False
    return True

def playThemeMusic(musicFile):

    '''
    Purpose: Play theme music in background
    Parameters:
        - musicFile (str): The music file to play
    
    Returns: None
    '''

    installed = installPyGame()
    if installed:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(musicFile)
        pygame.mixer.music.play(-1)
    #pygame.mixer.music.pause()
    #pygame.mixer.music.stop()

def createGameandDisplay():

    '''
    Purpose: createGameandDisplay
    Parameters: None
    
    Returns: Display and Game instances
    '''

    gameInstance = Game()
    displayInstance = MainDisplay()
    return gameInstance, displayInstance

def startThreads(displayInstance, gameInstance):

    '''
    Purpose: To create and start threads of execution
    Parameters:
        - displayInstance (MainDisplay): The display instance
        - gameInstance (Game): The game instance
    
    Returns: None
    '''

    displayThread = Thread("displayThread", 1, displayInstance.updateScene, gameInstance)
    gameplayThread = Thread("playthread", 2, gameInstance.playGame, displayInstance)
    gameplayThread.startThread()
    displayThread.startThread()

def main():

    playThemeMusic('HarryPotterTheme.mp3')
    #gameInstance, displayInstance = createGameandDisplay()
    #import time
    #time.sleep(60)
    #displayInstance.getMouse()

    # startThreads(displayInstance, gameInstance)
    
if __name__ == "__main__":
    main()