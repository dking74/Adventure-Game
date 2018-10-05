from enum import Enum
from display import MainDisplay, DisplayState

class GameState(Enum):
    START = 1
    PLAYING = 2
    PAUSED = 3
    END = 4

class Game():

    '''
    Class name: Game 
    Class Purpose: To play a game of "The Search for Horcruxes"
    '''

    def __init__(self):

        '''
        Purpose: To initialize the game
        Parameters: None
        
        Returns: None
        '''

        self.mainCharacter = ""
        self.bestFriend = ""
        self._state = GameState.START
        self.displayInstance = MainDisplay()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, newState):
        self._state = newState

    @staticmethod
    def playGame():
        pass