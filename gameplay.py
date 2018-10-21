from enum import Enum
from thread import threadSemaphore
from situations import *
from characters import *
from fight import Fight
import time
import random

class GameState(Enum):
    NOTYET = 0
    PLAYING = 1
    RESULT = 2
    AGAIN = 3
    END = 4

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
        self._continueMessage = None
        self._eventType = None
        self._userInput = None
        self._action = None
        self.fight = None
        self._wins = 0
        self._losses = 0
        self._totalMovesMade = 0
        self._averageMoveCount = 0
        self._stepsLeft = 10
        self._horcruxesLeft = 3
        self._enemiesLeft = 2
        self._againMessage = ""
        self._lastResult = ""
        self._horcruxesCaptured = []

    def __repr__(self):

        """Provide a string representation of the instance"""
        return "Game(Character='{}', State='{}', Wins='{}', Losses='{}')".format(self.character.characterName, self._state, self._wins, self._losses)

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

    @property
    def horcruxCount(self):

        """Getter to get the horcrux found number"""
        return self._horcruxesLeft

    @horcruxCount.setter
    def horcruxCount(self, newCount):

        """Setter to change the horcrux count"""
        self._horcruxesLeft = newCount

    @property
    def enemiesLeft(self):

        """Getter to determine if enemy limit has been reached"""
        return self._enemiesLeft

    @enemiesLeft.setter
    def enemiesLeft(self, newCount):

        """Setter to set new enemy count"""
        self._enemiesLeft = newCount

    def setResultMessage(self, resultMessage):

        """Setter to set the result of the game"""
        self._lastResult = resultMessage

    def setUserInput(self, inputMessage):

        """Setter for the function input"""
        self._userInput = inputMessage

    def setContinueInput(self, inputMessage):

        """Setter to determine if user wants to continue"""
        self._continueMessage = inputMessage

    def getDisplayMessage(self):

        """Returns the current display message for 
           game"""
        return self._displayMessage

    def getEventType(self):

        """Returns the curret event type for the game"""
        return self._eventType

    def getStepsLeft(self):

        """Returns the number of steps left"""
        return self._stepsLeft

    def _shouldGenerateNewMessage(self, displayInstance):

        """Function to determine if new game message should be generated"""
        hasMessageBeenPrinted = displayInstance.isMessagePrinted
        print("Has message been printed: " + str(hasMessageBeenPrinted))

        # wait until message has been printed
        while not hasMessageBeenPrinted:
            print("Checking message been printed")
            hasMessageBeenPrinted = displayInstance.isMessagePrinted

        # now change status of flag back to false
        threadSemaphore.lock()
        displayInstance.isMessagePrinted = False
        threadSemaphore.unlock()

    def _generateGameSituation(self, displayInstance):

        """Function that generates a situation for the user to be in"""
        threadSemaphore.lock()
        self._continueMessage = ""
        situationChoice = random.choice([obstacles, downgrades, horcruxes, enhancements])
        possibleChoices = [message for message in situationChoice['data']]
        message = random.choice(possibleChoices)

        while self._displayMessage == message:
            message = random.choice(possibleChoices)
        
        # set event type and display message to access in display
        # decrease the number of steps the user has
        self._eventType = situationChoice['type']
        self._displayMessage = message[0]
        self._action = message[1]
        self._stepsLeft = self._stepsLeft - 1
        self._updateOnAction(message)
        threadSemaphore.unlock()

    def _updateOnAction(self, message):

        """If a situation has an action associated, take that action"""

        def takeAction(positive):

            """Take action appropriate for category"""
            keyAction = list(self._action.keys())[0] 
            valAction = list(self._action.values())[0]
            addVal = valAction if positive else -valAction
            if keyAction == 'health':
                self.character.characterHealth = self.character.characterHealth + addVal
            elif keyAction == 'power':
                self.character.characterPower = self.character.characterPower + addVal
            elif keyAction == 'smarts':
                self.character.characterSmarts = self.character.characterSmarts+ addVal    

        if self._eventType == 'enhancements':
            takeAction(True)
        elif self._eventType == 'downgrades':
            takeAction(False)
        elif self._eventType == 'horcruxes':
            horcruxes['data'].remove(message)
            self._horcruxesCaptured.append(message)

    def _fightEnemy(self, enemyName, enemyStats, characterPlaying):

        '''
        Purpose: To handle fighting an enemy
        Parameters:
            - enemyName (str): The name of the enemy
            - enemyStats (dict): The stats of the enemy
            - characterPlaying (Character): The character that was chosen
        Returns: None
        '''

        self.fight = Fight(enemyName, enemyStats, characterPlaying)
        self.fight.fight()
        if self.fight.fightResult == 'win':
            self._enemiesLeft -= 1

    def _noFightSelected(self):

        """For when the user selects he does not wish to fight"""
        self.character.characterHealth -= 20
        self.character.characterPower -= 1
        #threadSemaphore.unlock()

    def _horcruxChange(self):

        """To handle a horcrux event
           decrease horcrux count and remove horcrux"""
        self._horcruxesLeft -= 1

    def _handleGameSituation(self, displayInstance):

        """Function that determines how to handle the
           given game situation"""
        threadSemaphore.lock()
        print("Inside game situation lock")
        if self._eventType == 'obstacles' and self._userInput == '1':
            self._fightEnemy(self._action, enemies[self._action], self.character)
        elif self._eventType == 'obstacles' and self._userInput == '2':
            self._noFightSelected()
        threadSemaphore.unlock()

        #determine if game should be ended
        # wait for continue message to be set in display
        print("Continue message is: " + str(self._continueMessage))
        while self._continueMessage == "" and self._stepsLeft != 0: {}
        print("Continue message after is: " + str(self._continueMessage))
        self._endGame()

    def _endGame(self):

        """Function to end the game and send
           signal to display to do so"""
        threadSemaphore.lock()
        if self._continueMessage == 'n' or \
           self._horcruxesLeft == 0 or \
           self._enemiesLeft == 0 or \
           self.character.characterHealth <= 0 or \
           self._stepsLeft == 0:
            self._state = GameState.RESULT
        self._continueMessage = ""
        threadSemaphore.unlock()

    def _reinitializeBeginning(self):

        """Function to reinitialize character back to normal"""
        self.character.characterHealth = 75
        self.character.characterPower = 5
        self.character.characterSmarts = 5
        self.character.characterName = ""
        self._displayMessage = ""
        self._continueMessage = ""
        self._eventType = ""
        self._userInput = ""
        self._action = ""
        self.fight = None
        self._stepsLeft = 10
        self._horcruxesLeft = 3
        self._enemiesLeft = 2
        self._againMessage = ""
        self._lastResult = ""
        self.state = GameState.NOTYET

        # this has to be reinitialized because deleting components of
        # horxcruxes during program so two aren't used
        for horcrux in self._horcruxesCaptured:
            horcruxes['data'].append(horcrux)

    def _newGameStats(self):

        """Function to update game statistics"""
        if self._lastResult == "win": 
            self._wins += 1
        else: 
            self._losses += 1
        self._totalMovesMade += (10 - self._stepsLeft)
        self._averageMoveCount = self._totalMovesMade / (self._wins + self._losses)

    def _playAgain(self):

        """Function to determine if should play again"""
        if self._againMessage == 'y':
            self._reinitializeBeginning() 
        else:
            self._state = GameState.END

    def playGame(self, displayInstance):
        
        """Run the game until the end has reached"""
        while self._state != GameState.END:
            if self._state == GameState.PLAYING:
                # send a message to display
                print("About to generate game situation")
                self._generateGameSituation(displayInstance)
                print("Generated game situation")
                # sleep briefly to allow other thread to take control of semaphore
                time.sleep(.1)
                # receive user input from display
                print("About to handle game situation")
                self._handleGameSituation(displayInstance)
                print("Handled game situation")
                time.sleep(.1)
            elif self._state == GameState.RESULT:
                time.sleep(.1)
                threadSemaphore.lock()
                self._newGameStats()
                self._state = GameState.AGAIN
                threadSemaphore.unlock()
            elif self._state == GameState.AGAIN:

                # wait until again message received
                while self._againMessage == "": {}

                threadSemaphore.lock()
                self._playAgain()
                threadSemaphore.unlock()
                time.sleep(.5)  
            time.sleep(.1)