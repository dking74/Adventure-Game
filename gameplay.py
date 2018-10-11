from enum import Enum
from display import *
from situations import *
from characters import *

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
        Parameters: 
            - displayInstance (MainDisplay): An instance of the main display
        
        Returns: None
        '''

        self.mainCharacter = ""
        self.bestFriend = ""
        self._state = GameState.START

    @property
    def state(self):

        """Getter to get state of game"""
        return self._state

    @state.setter
    def state(self, newState):

        """Setter to set state of game"""
        self._state = newState

    def playGame(self, displayInstance):
        
        """Run the game until the end has reached"""
        while self._state != GameState.END:
            self._state = GameState.END
            pass