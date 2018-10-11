import graphics
from graphics import Image, Point, Rectangle, Entry, Text
from widgets import MyButton, defineProps
from music import Music
from enum import Enum
from gameplay import *
import tkinter
import datetime

#properties of a general button
buttonProps = {
    'highlightthickness': '2px', 
    'highlightbackground': 'black', 
    'width': 9, 
    'height': 2,
    'background': 'black',
    'relief': 'sunken'
}

# states of a display
class DisplayState(Enum):
    START = 0
    REGPLAY = 1
    PAUSED = 2
    GOODNEWS = 3
    BADNEWS = 4
    WIN = 5
    LOSE = 6
    AGAIN = 7
    END = 8

class MainDisplay(graphics.GraphWin):

    '''
    Class name: Display 
    Class Purpose: To show the game play features
    Inherits: graphics.GraphWin (a class for display features)
    '''

    def __init__(self, width=600, height=600, backgroundImage="HarryPotter.png", title="The Search for Horcruxes"):

        '''
        Purpose: To initialize a display object
        Parameters:
            - backgroundImage (str): The name of the background image to display
            - width (int): optional: The width of the screen
            - height (int): optional: The height of the screen
            - title (str): optional: The title for the screen
        
        Returns: None
        '''

        super().__init__(title, width, height)
        self.pack_propagate(0)
        self._dislayState = DisplayState.START
        self._backgroundImage = backgroundImage
        self._createButtons('Exit Game', 'Pause Game', 'Stop Music')
        self._createBackground(Point(self.getWidth()/2, self.getHeight()/2))

    def _createBackground(self, location):

        """Create background image for window"""
        newImage = Image(location, self._backgroundImage)
        newImage.draw(self)

    def _defineButtons(self, *buttonNames):

        """Define the button structures"""
        exitButton = pauseButton = stopMusicButton = None
        try:
            exitButton = MyButton(self, buttonNames[0], **buttonProps)
            pauseButton = MyButton(self, buttonNames[1], **buttonProps)
            stopMusicButton = MyButton(self, buttonNames[2], **buttonProps) 

            # position the buttons
            exitButton.place(x=15, y=8)
            pauseButton.place(x=510, y=8)
            stopMusicButton.place(x=510, y=50)
        except IndexError:
            pass  
        return exitButton, pauseButton, stopMusicButton

    def _createButtons(self, *buttonNames):

        """Manages buttons on main display"""

        # create the buttons and return the button instances
        exitButton, pauseButton, stopMusicButton = self._defineButtons(*buttonNames)

        # create callback for each initial button
        def exitPressed():
            exitButton.lastClick = datetime.datetime.now().time()
            exitButton.pressed = not exitButton.pressed
            self.close()
            import sys
            sys.exit()

        def pausePressed():
            pauseButton.lastClick = datetime.datetime.now().time()
            pauseButton.pressed = not pauseButton.pressed
            print("paused")

        def stopPressed():
            stopMusicButton.lastClick = datetime.datetime.now().time()
            stopMusicButton.pressed = not stopMusicButton.pressed
            if stopMusicButton.pressed:
                Music.resumeMusic()
                stopMusicButton.buttonName = "Stop Music"
            else:
                Music.pauseMusic()
                stopMusicButton.buttonName = "Play Music"

        # configure the buttons callback
        exitButton.callbackFunc = exitPressed
        pauseButton.callbackFunc = pausePressed               
        stopMusicButton.callbackFunc = stopPressed

    @property
    def state(self):

        """Getter for the state of the display"""
        return self._dislayState

    @state.setter
    def state(self, newState):

        """Setter for the state of the display"""
        self._dislayState = newState

    def _showWelcomeScreen(self, messageBoxTop, messageBoxBottom, **props):

        '''
        Purpose: To provide a welcome message to user
        Parameters:
            - messageBoxTop (Point): The top left point of box
            - messageBoxBottom(Point): The bottom right point of box
            - props (dict): Properties of message box
        
        Returns: None
        '''

        rectangleBox = Rectangle(messageBoxTop, messageBoxBottom)
        defineProps(rectangleBox, fill='black', outcolor='white', outwidth=3)
        #textBox = Text()
        rectangleBox.draw(self)
        return rectangleBox

    def _initializeDisplay(self):

        """Initialize the display with a welcome message and
           allowing the individiual to choose their character"""
        welcomeBox = self._showWelcomeScreen(Point(self.getWidth()/2 - 200, self.getHeight()*3/4 - 100),
                                             Point(self.getWidth()/2 + 200, self.getHeight()*3/4 + 100))
        return welcomeBox

    def updateScene(self, gameInstance):
        
        """Update scene until we are at the end;
            Start with initialization"""
        welcomeBox = self._initializeDisplay()
        while self._dislayState != DisplayState.END:
            self._dislayState = DisplayState.END
            if self._dislayState == DisplayState.START:
                pass
            elif self._dislayState == DisplayState.REGPLAY:
                pass
            elif self._dislayState == DisplayState.PAUSED:
                pass
            elif self._dislayState == DisplayState.GOODNEWS:
                pass
            elif self._dislayState == DisplayState.BADNEWS:
                pass
            elif self._dislayState == DisplayState.WIN:
                pass
            elif self._dislayState == DisplayState.LOSE:
                pass
            elif self._dislayState == DisplayState.AGAIN:
                pass

class SubDisplay(graphics.GraphWin):

    """Class to display sub object screens based on main screen"""
    def __init__(self):
        pass