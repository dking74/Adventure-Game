from enum import Enum
from situations import *
from characters import *

class GameState(Enum):
    NOTYET = 0
    PLAYING = 1
    PAUSED = 2
    END = 3

class Game():

    '''
    Class name: Game 
    Class Purpose: To play a game of "The Search for Horcruxes"
    '''

    def __init__(self):

        '''
        Purpose: To initialize the game to be able to play
        Parameters: None
        Returns: None
        '''

        self.character = Character()
        self._state = GameState.NOTYET
        self._displayMessage = None
        self._wins = 0
        self._losses = 0
        self._averageMoveCount = 0

    def __repr__(self):

        """Provide a string representation of the instance"""
        return "Game(Character='{}', State='{}', Wins='{}', Losses='{}')".format(self._character.characterName, self._state, self._wins, self._losses)

    @property
    def state(self):

        """Getter to get state of game"""
        return self._state

    @state.setter
    def state(self, newState):

        """Setter to set state of game"""
        self._state = newState

    @property
    def wins(self):

        """Get the current win count"""
        return self._wins

    @property
    def losses(self):

        """Get the current loss count"""
        return self._losses

    @property
    def moveCount(self):

        """Get the average move count
           to win or lose"""
        return self._averageMoveCount

    def getDisplayMessage(self):

        """Returns the current display message for 
           game"""
        return self._displayMessage

    def _generateGameSituation(self):

        """Function that generates a situation for the user to be in"""
        pass

    def playGame(self, displayInstance):
        
        """Run the game until the end has reached"""
        while self._state != GameState.END:
            if GameState.PLAYING:
                pass
            elif GameState.PAUSED:
                pass

class Character():

    """Class to handle character attributes"""
    def __init__(self):
        self._characterName = ""
        self._characterStrength = ""
        self._characterHealth = 50
        self._characterPower = 50
        self._characterSmarts = 50

    @property
    def strength(self):

        """Get the character strength"""
        return self._characterStrength

    @strength.setter
    def strength(self, strength):

        """Set the character strength"""
        self._characterStrength = intToStrength[strength]

    @property
    def characterName(self):

        """Getter to get the current character name"""
        return self._mainCharacter

    @characterName.setter
    def characterName(self, characterName):

        """A setter to set the character name"""
        self._mainCharacter = characterName

# dictionary to convert number to strength
intToStrength = {
    '1': 'Health',
    '2': 'Power',
    '3': 'Smarts'
}