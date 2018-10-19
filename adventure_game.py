################################################################################################
#
#	Creator : Devon King
#	Purpose : To create a program that plays a game
#
#	Course  : SWDV 600
#	Date    : 10/6
#   Notes   : This program contains dependencies...
#           : This will not work without them
#           : One dependency is pygame (The program should
#           : install it upon startup, but if not will
#           : need to be installed to work).
#           : The program should run without errors, but
#           : if one occurs, it is due to data exchange in threads
#
#   Extra Credit Reasons:
#       1. Created a full-fledged GUI to interact with user
#       2. Added music features to be able to start and stop the music
#       3. Program is multithreaded and communicates between threads with semaphores
#       4. Put a lot of background work to make it functional
#       5. Used clever decorators for error checking input
#       6. Created a menu to stop the game, as well as see key features of the game
#       7. Create a class for flashing text, so text is dynamic and appears as if 
#          it is being typed to. Additionally, multiple text can be printed at same time
#       8. Created state machines for display and game to handle the synchronization and states
#           of the two threads
#
#       These are just a few reasons I believe I deserve extra credit;
#       I don't think any other student put as much effort into this as I did
#
#   Disclaimer:
#       I am sure there are going to be features that do not work quite how I want them to
#       While I used some threading features, the limitation of not be able to run additional
#       threads from within the main thread to update the GUI limits the performance and
#       expected results greatly. While the program works great on my machine, I am not sure
#       how it will perform on a different system, since I was forced to use small timing
#       mechanisms (which is never a great approach). Given more time, I could account for
#       this and create a much more reliable program.
#
#       When testing the program on a Windows computer, my flashing text is able to be deleted
#       much quicker than when on my mac. This could create a timing issue in when the messages
#       are displayed.
#
#       Additionally, 'pygame' is needed. The program should be able to install it for you,
#       but if not, the music will not play how it is supposed to.
#
##############################################################################################

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