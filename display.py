import graphics
from enum import Enum
from gameplay import Game, GameState

class DisplayState(Enum):
    START = 0
    REGPLAY = 1
    PAUSED = 2
    GOODNEWS = 3
    BADNEWS = 4
    WIN = 5
    LOSE = 6
    AGAIN = 7

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
        self.gameInstance = Game()

    @staticmethod
    def updateScene():
        pass


