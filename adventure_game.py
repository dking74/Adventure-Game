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
#           : need to be installed to work correctly).
#           : The program should run without errors, but
#           : if one occurs, it is due to data exchange in threads
#        UPDATE: 
#           : The program will work without pygame, but exception is thrown
#
#   ADDITIONALLY:
#           : I kind of made an interesting design choice in letting
#           : the GUI drive the behavior of the background threads.
#           : This is how it normally works, but I don't think I had
#           : the best plan at the start in how to share variables
#           : and change the state machine in the game thread. As a result,
#           : I think I kind of eliminated some encapsulation features by
#           : exposing instance variables of the game thread too much.
#           : While this generally needs to occur with threads, so that
#           : data is available between them, I think I could have done a 
#           : much better job of hiding variables and only exposing them within
#           : the class itself. The Display class also could be broken up better
#           : into separate classes to better understand the class itself, but
#           : I ran out of time to do this. With more time, the code would look
#           : much cleaner, would be more practical and maintable, and more scalable.
#           : I also had stretches where I was inconsistent in how I update variables...
#           : I believe I update sometimes in Display class and others in the Game class.
#           : That being said, the code is still decently written, with some flaws along the way
#           : from a professional perspective.
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
#       9. Appropriate separation of concerns, following a MVC pattern by separating the display
#          option and the data option
#
#       These are just a few reasons I believe I deserve extra credit;
#       I don't think any other student put as much effort into this as I did --> Approximately 35 hours
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
#       are displayed. I would not consider this program 'thread-safe' in the early stages of 
#       development, and much more testing would be needed to perfect this program.
#
#       There is also a difference in timing and formatting between computers... Tested on 
#       Windows, Linux, and mac, and it works on all of them, but the formatting of letters is 
#       platform dependent; I can't really combat that at all. Moving forward, sleeps should
#       be taken out and better concurrency methods should be taken.
#
#       Additionally, 'pygame' is needed. The program should be able to install it for you,
#       but if not, the music will not play how it is supposed to.
#
#       ONE MORE TIME, I DO NOT GUARANTEE THIS PROGRAM ON A DIFFERENT SYSTEM;
#       I HAVE GOTTEN MIXED RESULTS ON DIFFERRENT SYSTEMS. IT SHOULD WORK MOSTLY
#       BUT TIMING IS BOUND TO BE OFF DEPENDING ON SYSTEM
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
        presses CTRL+C. This is needed because program is running
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