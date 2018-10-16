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
import signal
import os

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

def exitSystem(signal, frame):

    """Function to catch a signal interrupt
        and to exit the program;
        This is used to pleasantly exit the system if the user
        presses CNTRL+C. This is needed because program is running
        multiple threads, and if key is pressed in middle, exceptions are thrown
        This is used to protect against that happening."""
    os._exit(1)


def startThreads(gameInstance, displayInstance, musicInstance):

    '''
    Purpose: To create and start threads of execution
    Parameters:
        - displayInstance (MainDisplay): The display instance
        - gameInstance (Game): The game instance
        - musicInstance (Music): The music player
    
    Returns: None
    '''

    signal.signal(signal.SIGINT, exitSystem)
    musicThread = Thread("musicThread", 3, musicInstance.playThemeMusic, displayInstance)
    gameplayThread = Thread("playthread", 2, gameInstance.playGame, displayInstance)
    displayInstance.updateScene(gameInstance)

def main():

    # initialize game
    gameInstance, \
    displayInstance, \
    musicInstance = createGameandDisplay('HarryPotterTheme.mp3')

    # start worker threads --> main gui thread has to run in main loop
    startThreads(gameInstance, displayInstance, musicInstance)
    
if __name__ == "__main__":
    main()