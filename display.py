import graphics
from graphics import Image, Point
from enum import Enum
from gameplay import *

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
        self._dislayState = DisplayState.START
        self._backgroundImage = backgroundImage
        self._createBackground(Point(self.getWidth()/2, self.getHeight()/2))

    def _createBackground(self, location):

        """Create background image for window"""
        newImage = Image(location, self._backgroundImage)
        newImage.draw(self)

    @property
    def state(self):

        """Getter for the state of the display"""
        return self._dislayState

    @state.setter
    def state(self, newState):

        """Setter for the state of the display"""
        self._dislayState = newState

    def updateScene(self, gameInstance):
        
        """Update scene until we are at the end"""
        while self._dislayState != DisplayState.END:
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