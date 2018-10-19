import graphics
from graphics import Image, Point, Rectangle, Entry, Text, color_rgb
from widgets import MyButton, defineProps, defineTextProps, buttonProps
from music import Music
from enum import Enum
from gameplay import GameState
from fight import spells
from situations import obstacles, enhancements, downgrades, horcruxes
from thread import threadSemaphore
import tkinter
import datetime
import time
import os

# decorator to check input values
# acceptable input values is parameter1
# position to place error message is second
def errorCheckText(position, validValues=None):
    def check(func):
        def wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            errorTextField = None

            # if not valid, print text indicating
            if validValues:
                while value not in validValues:
                    errorTextField = Text(position, "Invalid Value entered. Try again.")
                    defineTextProps(errorTextField, textcolor='red', size=12)
                    errorTextField.draw(args[0])
                    value = func(*args, **kwargs)
                    
                    # Text Field was drawn; remove it
                    if errorTextField != None:
                        errorTextField.undraw()
            return value
        return wrapper
    return check

# states of a display
class DisplayState(Enum):
    START = 0
    REGPLAY = 1
    RESULT = 2
    AGAIN = 3
    END = 4

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
        self._oldState = DisplayState.END
        self._currentState = DisplayState.START
        self._backgroundImage = backgroundImage

    @property
    def state(self):

        """Getter for the state of the display"""
        return self._dislayState

    @state.setter
    def state(self, newState):

        """Setter for the state of the display"""
        self._dislayState = newState

    def _createBackground(self, location):

        """Create background image for window"""
        newImage = Image(location, self._backgroundImage)
        newImage.draw(self)

    def _defineButtons(self, *buttonNames):

        """Define the button structures"""
        self._exitButton = self._pauseButton = self._stopMusicButton = None
        try:
            self._exitButton = MyButton(self, buttonNames[0], **buttonProps)
            self._pauseButton = MyButton(self, buttonNames[1], **buttonProps)
            self._stopMusicButton = MyButton(self, buttonNames[2], **buttonProps) 

            # set the pause button to initially inactive
            self._pauseButton.config(state='disabled')

            # position the buttons
            self._exitButton.place(x=15, y=8)
            self._pauseButton.place(x=510, y=3)
            self._stopMusicButton.place(x=510, y=45)
        except IndexError:
            pass 

    def _createButtons(self, gameInstance, *buttonNames):

        """Manages buttons on main display
           pass in game instance to view statistics of game"""

        # create the buttons and return the button instances
        self._defineButtons(*buttonNames)

        # create callback for each initial button
        def exitPressed():
            self._exitButton.lastClick = datetime.datetime.now().time()
            self._exitButton.pressed = not self._exitButton.pressed
            self.close()
            os._exit(1)

        def pausePressed():
            self._pauseButton.lastClick = datetime.datetime.now().time()
            self._pauseButton.pressed = not self._pauseButton.pressed
            updateButtonProps = buttonProps
            updateButtonProps['width'] = 50
            updateButtonProps['height'] = 2
            updateButtonProps['justify'] = tkinter.CENTER

            # create a separate display and give properties
            menuDisplay = SubDisplay(self, [], self._pauseButton)
            menuDisplay.config(width=450, height=450)
            aboutButton = MyButton(menuDisplay, "About Game", **updateButtonProps)
            aboutButton.config(command=lambda: aboutGame(aboutButton, menuDisplay))
            aboutButton.place(x=0, y=0)
            creatorButton = MyButton(menuDisplay, "About Creator", **updateButtonProps)
            creatorButton.config(command=lambda: aboutCreator(creatorButton, menuDisplay))
            creatorButton.place(x=0, y=50)
            statsButton = MyButton(menuDisplay, "Game Statistics", **updateButtonProps)
            statsButton.config(command=lambda: gameStats(gameInstance, statsButton, menuDisplay))
            statsButton.place(x=0, y=100)
            spellsButton = MyButton(menuDisplay, "View Spells", **updateButtonProps)
            spellsButton.config(command=lambda: spellsDisplay(spellsButton, menuDisplay))
            spellsButton.place(x=0, y=150)
            obstacleButton = MyButton(menuDisplay, "View Obstacles", **updateButtonProps)
            obstacleButton.config(command=lambda: situationDisplay(obstacles['data'], "Obstacles", obstacleButton, menuDisplay))
            obstacleButton.place(x=0, y=200)
            enhancementsButton = MyButton(menuDisplay, "View Enhancements", **updateButtonProps)
            enhancementsButton.config(command=lambda: situationDisplay(enhancements['data'], "Enhancements", enhancementsButton, menuDisplay))
            enhancementsButton.place(x=0, y=250)
            downgradeButton = MyButton(menuDisplay, "View Downgrades", **updateButtonProps)
            downgradeButton.config(command=lambda: situationDisplay(downgrades['data'], "Downgrades", downgradeButton, menuDisplay))
            downgradeButton.place(x=0, y=300)
            horcruxButton = MyButton(menuDisplay, "View Horcruxes", **updateButtonProps)
            horcruxButton.config(command=lambda: situationDisplay(horcruxes['data'], "Horcruxes", horcruxButton, menuDisplay))
            horcruxButton.place(x=0, y=350)
            MyButton(menuDisplay, "Exit Screen", **updateButtonProps, command=lambda:menuDisplay._destroyWindow()).place(x=0, y=400)

        def stopPressed():
            self._stopMusicButton.lastClick = datetime.datetime.now().time()
            self._stopMusicButton.pressed = not self._stopMusicButton.pressed
            if self._stopMusicButton.pressed:
                Music.resumeMusic()
                self._stopMusicButton.buttonName = "Stop Music"
            else:
                Music.pauseMusic()
                self._stopMusicButton.buttonName = "Play Music"

        # configure the buttons callback
        self._exitButton.callbackFunc = exitPressed
        self._pauseButton.callbackFunc = pausePressed               
        self._stopMusicButton.callbackFunc = stopPressed

    def _showTitleScreen(self, startPoint, text, **textProps):

        '''
        Purpose: To print the title to the top of the screen
        Parameters:
            - startPoint (Point): The starting point of the text
            - text (Text): The text to display

        Returns: The array of text objects
        '''

        # go through each text letter and print upwards until middle is reached
        # afterwards, print downwards
        currentPoint = startPoint
        middleTextLength = len(text) / 2
        textLocation = 0
        letters = []
        for textLetter in text:

            # apply shade and regular text
            letter1 = self.create_text(currentPoint.getX(), currentPoint.getY(), 
                                      text=textLetter,
                                      fill='black',
                                      font=('Helvetica', 50))
            letter2 = self.create_text(currentPoint.getX()+3, currentPoint.getY()+3, 
                                      text=textLetter,
                                      fill='gold',
                                      font=('Helvetica', 50))
            letters.append(letter1)
            letters.append(letter2)
            if textLocation <= middleTextLength:
                currentPoint = Point(currentPoint.getX() + 24, currentPoint.getY() - 7)
            else:
                currentPoint = Point(currentPoint.getX() + 24, currentPoint.getY() + 7)
            textLocation = textLocation + 1
        return letters

    def _showWelcomeScreen(self, messageBoxTop, messageBoxBottom, **props):

        '''
        Purpose: To provide a welcome message to user
        Parameters:
            - messageBoxTop (Point): The top left point of box
            - messageBoxBottom(Point): The bottom right point of box
            - props (dict): Properties of message box
        
        Returns: The beginning instances
        '''

        rectangleBox = Rectangle(messageBoxTop, messageBoxBottom)
        defineProps(rectangleBox, fill='black', outcolor='white', outwidth=3)
        rectangleBox.draw(self)
        welcomeText = (
            "Welcome to The Search for the Horcruxes! "
            "You are about to embark on a journey for the ages. "
            "This game will take you through the lives of Harry Potter and his friends. "
            "You will take on the same challenges as Harry did as you look to "
            "capture the horcruxes and defeat Voldemort. On your path to find the horcruxes, "
            "you will encounter villains and you must defeat them to move on. "
            "You must collect 3 horcruxes in order to win or defeat 2 enemies. "
            "Let's get started!"
        )
        welcomeMessage = FlashText(self, 
                                   welcomeText, 
                                   Point(rectangleBox.getP1().getX()+15,
                                         rectangleBox.getP1().getY()+15),
                                   .01, 50, 7, 15,
                                   textcolor='green')
        return rectangleBox, welcomeMessage

    def _showCopyrightMessage(self, startPosition, **props):

        '''
        Purpose: To print the copyright message of the game on the screen
        Parameters:
        Returns:
        '''
        copyrightSym = u"\u00A9"
        copyrightMessage = u"{} 2018 Devon King Maryville University".format(copyrightSym)
        copyMessage = Text(startPosition, copyrightMessage)
        defineTextProps(copyMessage, **props)
        copyMessage.draw(self) 
        
    def _initializeDisplay(self):

        """Initialize the display with a welcome message and
           allowing the individiual to choose their character"""

        titleText = self._showTitleScreen(Point(20, 120), "The Search For Horcruxes", size=90)
        welcomeBox, welcomeText = self._showWelcomeScreen(
                            Point(self.getWidth()/2 - 200, self.getHeight()*3/4 - 100),
                            Point(self.getWidth()/2 + 200, self.getHeight()*3/4 + 115))
        return titleText, welcomeBox, welcomeText

    def updateScene(self, gameInstance):

        """Main thread run to update scene of game"""

        # Update scene until we are at the end;
        # Initialize all variables needed first;
        # Also, create background, buttons, and copyright
        self._createBackground(Point(self.getWidth()/2, self.getHeight()/2))
        self._createButtons(gameInstance, 'Exit Game', 'Pause Game', 'Pause Music')
        self._showCopyrightMessage(Point(490, 580))

        # start updating screen until the end is reached
        while self._currentState != DisplayState.END:

            # make sure screen is still open; if not close app
            if self.isClosed():
                os._exit(1)

            # check the state and act appropriately
            stateChanged = self._stateChanged()
            if self._currentState == DisplayState.START and not stateChanged:
                self._startDisplay()
            elif self._currentState == DisplayState.REGPLAY and not stateChanged:
                self._playGame(gameInstance)  
            elif self._currentState == DisplayState.RESULT and not stateChanged:
                self._showGameResult(gameInstance)
            elif self._currentState == DisplayState.AGAIN and not stateChanged:
                self._showAgainScreen(gameInstance)
                time.sleep(2)
            time.sleep(.1)

    def _startDisplay(self):

        """Function to initialize display and setup game"""
        titleText, \
        welcomeBox, \
        welcomeText = self._initializeDisplay()

        # buttons are initially inactive; activate them
        self._pauseButton.config(state='normal')
        textEntered = self._askUserQuestion("Do you wish to continue? (y/n)",
                                                Point(welcomeBox.getP1().getX()+30, 
                                                        welcomeBox.getP2().getY()-40),
                                                ['y', 'n'], size=12)
        if textEntered == 'y':
            self._completeFuncAfterTime(4000, self._printMessage, "Great! Let's get started", Point(125, 375), 25, 15, 3500, .01)
            self._deleteObject(welcomeText)
            time.sleep(1)
            self._changeState(DisplayState.REGPLAY)
        else:
            self._closeProcess(welcomeText)     

    def _closeProcess(self, *deletingObjects):
    
        '''To close the thread and window, along with cleanup'''
        self._completeFuncAfterTime(4000, self._printMessage, "GOODBYE AND HAVE A NICE DAY!", Point(125, 400), 24, 15, 5000, .01)
        self._deleteObject(*deletingObjects)
        time.sleep(1)
        self._changeState(DisplayState.END)
        self.close()
        os._exit(1)

    def _changeState(self, newState):
            
        '''To update the state currently to old state'''
        self._oldState = self._currentState
        self._currentState = newState

    def _playGame(self, gameInstance):

        """Function that actually is responsible for playing game"""

        # get properties of character
        character = self._askUserQuestion("What is the character name? ", Point(150, 375), None, size=16)
        questionText = Text(Point(300, 375), "What attribute will be your characters strength?")
        defineTextProps(questionText, textcolor='green', size=16)
        questionText.draw(self)
        attribute = self._askUserQuestion("(1) Health (2) Power (3) Smart", Point(130, 400), ['1', '2', '3'], size=12)
        gameInstance.character.strength = attribute
        self._deleteObject(questionText)

        # Indicate game is beginning and prepare
        gameInstance.character.characterName = character
        self._printMessage("{}, your game is beginning...".format(character), Point(125, 375), 25, 12, 0, .01, size=18)
        time.sleep(1)
        self._updateGameScene(gameInstance)
        self._currentState = DisplayState.RESULT

    def _updateGameScene(self, gameInstance):
        
        """Function that loops continuously waiting for game to update
           to find the message to display"""

        # change the game state to be playing to start the other thread execution
        gameInstance.state = GameState.PLAYING
        self._lastMessage = None

        # dumb, but guarantee other thread obtains lock first
        # so that game message can be received first, then start
        time.sleep(.1)
        while gameInstance.state == GameState.PLAYING:
            threadSemaphore.lock()

            # check if game has ended after lock acquired
            if gameInstance.state == GameState.RESULT:
                break
        
            displayText = gameInstance.getDisplayMessage()
            eventType = gameInstance.getEventType()
            if displayText != self._lastMessage:
                self._lastMessage = displayText
                self._determineGameAction(gameInstance, displayText, eventType)

            threadSemaphore.unlock()
            time.sleep(.1)

    def _determineGameAction(self, gameInstance, displayText, eventType):

        """Determine what needs to be printed based on display text
           and event type; also ask user if they wish to continue"""

        if eventType == 'horcruxes' or eventType == 'enhancements' or eventType == 'downgrades':
            if eventType == 'horcruxes':
                gameInstance.horcruxCount -= 1
                displayText = displayText + " {} horcruxes remain".format(gameInstance.horcruxCount)
            self._printMessage(displayText, Point(125, 375), 40, 8, 2000, .01, 14)
            time.sleep(.1)
        elif eventType == 'obstacles':
            displayText = displayText + "Do you want to fight (1) or run (2)? "
            userInput = self._askUserQuestion(displayText, Point(125, 375), ['1', '2'])
            if userInput == '2':
                self._printMessage(
                   "The result of not fighting is a power deduction of 1 and health deduction of 20!",
                   Point(125, 375), 30, 10, 0, .01
                )
            gameInstance.setUserInput(userInput)
            threadSemaphore.unlock()
            time.sleep(.2)

            # have to check this input after other one because lock
            # has been given back to other thread so that messages 
            # can be generated for the fight result
            if userInput == '1':
                self._printFightMessages(gameInstance)

        # print the number of steps left to the user;
        # lock semaphore back up if obstacle event occurred
        if eventType == 'obstacles':
            threadSemaphore.lock()
        stepsLeft = gameInstance.getStepsLeft()
        if stepsLeft > 0:
            displayText = "You have {} steps left. Do you want to continue?".format(stepsLeft)
            userInput = self._askUserQuestion(displayText, Point(125, 485), ['y', 'n'])
            gameInstance.setContinueInput(userInput)

    def _printFightMessages(self, gameInstance):

        """Function that prints messages
           while fight is going on"""
        messageLocation = Point(125, 375)
        while gameInstance.fight.fightOn:
            threadSemaphore.lock()
            if not gameInstance.fight.fightOn:
                break
            self._printMessage(gameInstance.fight.fightMessage,
                               messageLocation,
                               30, 9, 2000, .01, 12)
            time.sleep(2)
            threadSemaphore.unlock()
            time.sleep(.1)
        
        threadSemaphore.lock()
        result = self._getFightResult(gameInstance)
        self._printMessage(result, messageLocation, 30, 9, 2000, .01, 12)
        time.sleep(2)
        threadSemaphore.unlock()

    def _getFightResult(self, gameInstance):

        """To print the result of the fight"""
        result = "The result of the fight was a {}. {} enemies left. ".format(gameInstance.fight.fightResult, gameInstance.enemiesLeft)
        if gameInstance.fight.fightResult == 'win':
            result += "20 health points have been given back to you!"
        return result

    def _showGameResult(self, gameInstance):
        
        """Displays the results of the game to user"""
        threadSemaphore.lock()
        result = ""
        if gameInstance.enemiesLeft == 0 or gameInstance.horcruxCount == 0:
            gameInstance.setResultMessage("win") 
            result = "WIN"
        else: 
            gameInstance.setResultMessage("loss")
            result = "LOSS"
        self._printMessage("The result of the game was: {}".format(result), 
                    Point(130, 420), 23, 15, 3000, .01, 25)
        time.sleep(3)
        self._currentState = DisplayState.AGAIN
        threadSemaphore.unlock()

    def _showAgainScreen(self, gameInstance):

        """Displays the 'play game again' screen
           and handles input"""
        threadSemaphore.lock()
        again = self._askUserQuestion("Do you want to play again? (y/n)", Point(130, 420), ['y', 'n'], 16)
        gameInstance.setAgainMessage(again)
        if again == 'y':
            self._currentState = DisplayState.REGPLAY
        else:
            self._printMessage("GOODBYE AND HAVE A NICE DAY!", Point(125, 400), 24, 15, 2000, .01)
            self._currentState = DisplayState.END
        threadSemaphore.unlock()

    def _printMessage(self, text, point, maxChar, xSpace, delay, textDelay, size=20):

        """Print a message on screen with properties"""
        tempTextElement = FlashText(
                                self,
                                text,
                                point,
                                textDelay, maxChar, xSpace+1, 20,
                                textcolor='green', size=size
                            )
        
        # delete text after some time
        self._completeFuncAfterTime(delay, tempTextElement.undraw)

    def _userMessage(self, text, locationStart, size=12):

        """Function to print if the user wish to continue and validates input
            - text (str): The text to display
            - locationStart (point): Where the message will start"""
        
        # create text field and entry for question
        textField = FlashText(self, 
                              text, 
                              locationStart, 
                              0, 40, 8, 20, 
                              textcolor='green', 
                              size=size)
        entryField = Entry(textField.getEndTextLocation(), 7)
        defineProps(entryField, fill='white')
        entryField.draw(self)
        return textField, entryField

    def _stateChanged(self):

        """Checks to see if the state of the display has changed;
            happens if the old state doesn't equal the new state"""
        if self._currentState == self._oldState:
            return True
        return False

    def _deleteObject(self, *objectDelete):

        """Deletes the inputted object(s)
            whether Tkinter or graphics.py object"""
        for objects in objectDelete:
            try:
                objects.undraw()
            except:
                self.delete(objects)

    def _completeFuncAfterTime(self, timeInterval, function, *args):

        '''
        Purpose: To register a callback on window after certain time
        Parameters:
            - timeInterval (int): The ms count to wait before callback
            - function (function): The function to run on the count
            - args (list): Arguments to supply to function
        Returns: None
        '''

        self.after(timeInterval, function, *args)

    def _askUserQuestion(self, text, location, options, size=12):

        """Kind of weird way to do this, but 
           want to user wrapper to check any input possible;
           this returns the input by user"""

        question, entry = self._userMessage(text, location, size)

        @errorCheckText(Point(300, 550), options)
        def askQuestion(window, field): 
            return self._waitUntilEnter(field)

        userInput = askQuestion(self, entry)
        self._deleteObject(question, entry)
        return userInput

    def _waitUntilEnter(self, textField):

        """Function that gets the input from the user"""
        key = ''
        while key != 'Return':
            try:
                key = self.getKey()
            except:
                os._exit(1)
        textEntered = textField.getText()
        textField.setText('')
        return textEntered

class SubDisplay(tkinter.Toplevel):

    """Class to display sub object screens based on main screen"""
    def __init__(self, window, components, buttonTrigger=None, title="Menu Screen", **kwargs):

        '''
        Purpose: Initialization of a Sub Display screen
        Parameters:
            - window (GraphWin): The window to have as parent
            - components (list): A list of dictionaries of all components on the display
            - buttonTrigger (Button): The button that triggered display
            - title (str): The title of the display
            - kwargs (dict): The keyword args to provide to sub display
        Returns: None
        '''

        super().__init__(window, **kwargs)
        self._parent = window
        self.title(title)
        self._triggeredButton = buttonTrigger
        if self._triggeredButton:
            self._triggeredButton.config(state='disabled')
        self._components = components
        self._drawComponents()
        self.protocol("WM_DELETE_WINDOW", self._destroyWindow)

    @property
    def components(self):

        """Getter to get components of class"""
        return self._components

    def setComponent(self, locationComp, newComponent):

        """Setter to set specific component in list"""
        try:    
            self._components[locationComp] = newComponent
        except IndexError:
            pass

    def addComponent(self, newComponent):

        """Add specific component to component list"""
        self._components.append(newComponent)
        self._drawComponents()

    def addComponents(self, *components):

        """Add list of components to components list"""
        for component in components:
            self.addComponent(component)

    def _drawComponents(self):

        """Draw the components on sub display"""
        for arg in self._components:
            try:

                # if element not already placed, place it
                if arg['element'] not in self.items:   
                    arg['element'].draw(self)
            except Exception as detail:
                pass      
            try:
                defineProps(arg['element'], **arg['props'])
                defineTextProps(arg['element'], **arg['props'])
            except:
                pass

    def _deleteComponents(self, *componentsLocation):

        """Delete specific components of list;
           componentsLocation is list of indices of components to lose"""
        for component in componentsLocation:
            try:
                del component
                self._drawComponents()
            except:
                pass
        
    def hideWindow(self):

        """Close the current window"""
        self.withdraw()

    def showWindow(self):

        """Reshow current window"""
        self.deiconify()

    def _destroyWindow(self):

        """After opening window, restores window back"""
        self.destroy()
        try:
            self._parent.showWindow()
        except:
            pass
        if self._triggeredButton:
            self._triggeredButton.config(state='normal')

class FlashText():

    """Class that displays Text field in a delayed fashion"""
    def __init__(self, window, text, startPosition, delay, restartNum, spaceX, spaceY, **props):

        """To initialize a flashing text instance
            - window (GraphWin): The parent window for object
            - text (str): The text to display
            - delay (float): The delay between displaying text
            - startPosition (Point): The first character point
            - props (dict): The props for the text"""

        self._window = window
        self._text = text
        self._delay = delay
        self._startPostion = startPosition
        self._props = props
        self._characters = []
        self._lastPosition = self._startPostion
        self._displayText(spaceX, spaceY, restartNum)

    def __str__(self):

        """Provide string representation of object"""
        return "FlashText('{}')".format(self._text)

    def getCharactersDrawn(self):

        """Returns the list of characters drawn"""
        return self._characters

    def _displayText(self, spaceX, spaceY, restartNum=None):

        """Display the text by iterating
           through every character in the sequence"""
        currentPosition = self._startPostion
        currentCharNum = 0
        for character in self._text:

            # end of the rectangle box; restart counter to print on next line --> if restart is provided
            if restartNum:
                if currentCharNum == restartNum:
                    currentCharNum = 0
                    currentPosition = Point(self._startPostion.getX(), currentPosition.getY()+spaceY)

            # create the text character and give props
            textElement = Text(currentPosition, character)
            defineTextProps(textElement, **self._props)
            
            # draw, but protect against user closing window
            try:    
                textElement.draw(self._window)
            except:
                os._exit(1)
            self._characters.append(textElement)
            currentPosition = Point(currentPosition.getX()+spaceX, currentPosition.getY())
            currentCharNum = currentCharNum + 1
            time.sleep(self._delay)
        self._lastPosition = currentPosition

    def getEndTextLocation(self):

        """Method to get the location of the last text drawn"""
        return Point(self._lastPosition.getX()+40, self._lastPosition.getY()+5)

    def undraw(self):

        """Undraw the objects"""
        for character in self._characters:
            character.undraw()
            time.sleep(self._delay)


# The below are functions with a specific purpose of producing
# sub screens associate with the menu screen; They are expected
# to have a short life span and are triggered when the appropriate button is pressed

subScreenProps = {
    'foreground': 'green',
    'background': 'black'
}

def aboutGame(button, parentWindow):

    """Display information about the game"""
    gameInfo = (
        "\n\nThe Search For Horcruxes is a text based game that is based on\n"
        "the 'Harry Potter' movies. The game is won by finding 3 Horcruxes or by\n"
        "defeating 2 enemies. A horcrux is an item that holds Lord Voldemort's\n"
        "(Harry's nemesis) soul. You have ten moves to find these horcruxes, but\n"
        "will find this difficult, as you will face Voldemort's followers. When you\n"
        "face a follower, you will be faced with a decision to fight or run. Fighting\n"
        "gives the chance to earn points back and win the game, but losing\n"
        "will lose points for you. Running will not allow these benefits.\n"
        "This a fun game for Pottermores!\n\n\n"
    )
    parentWindow.withdraw()
    display = SubDisplay(parentWindow, [], button, title="About Game", height=200, width=200)
    display.addComponents(
        {
            'element': tkinter.Label(display, text=gameInfo, **subScreenProps).pack()
        }
    )

def aboutCreator(button, parentWindow):

    """Display information about me, the creator"""
    creatorInfo = (
        "\n\nThe creator of the game is Devon King, who is a\n"
        "Master's of Software Development student as of 2018.\n"
        "He obtained his Bachelor's of Computer Engineering with an\n"
        "emphasis in Robotic Technology, with minors in Mathematics\n"
        "and Computer Science at the University of Missouri-Columbia\n"
        "in May of 2018. As of the creation of this game, he lives with his\n"
        "wife in Mehlville, MO. He currently resides at Ameren working\n"
        "on web service technology.\n\n\n"
    )
    parentWindow.withdraw()
    display = SubDisplay(parentWindow, [], button, title="About Creator", height=200, width=200)
    display.addComponents(
        {
            'element': tkinter.Label(display, text=creatorInfo, **subScreenProps).pack()
        }
    )

def gameStats(gameInstance, button, parentWindow):

    """Use the information from the game to get the game stats
       and display those stats to a sub screen"""
    statInfo = (
        "\nWINS: {}\n\n"
        "LOSSES: {}\n\n"
        "AVERAGE MOVES: {}\n".format(gameInstance.wins, gameInstance.losses, gameInstance.moveCount)    
    )
    parentWindow.withdraw()
    display = SubDisplay(parentWindow, [], button, title="Game Stats", height=200, width=200)
    display.addComponents(
        {
            'element': tkinter.Label(display, text=statInfo, padx=100, pady=100, **subScreenProps).pack()
        }
    )

def spellsDisplay(button, parentWindow):

    """Use information from spells dictionary to print to screen"""
    message = ""
    for spell in spells:
        tempMessage = "%-20s:          %s points" % (list(spell.keys())[0], str(list(spell.values())[0]))
        message += "%-s\n" % tempMessage#str(list(spell.values())[0]))
    parentWindow.withdraw()
    display = SubDisplay(parentWindow, [], button, title="Spells")
    display.addComponents(
        {
            'element': tkinter.Label(display, width=30, anchor=tkinter.W, text=message, justify=tkinter.LEFT, **subScreenProps).pack(side=tkinter.LEFT, expand=tkinter.NO)
        }
    )

def situationDisplay(dictionaryList, title, button, parentWindow):

    """Use information from specific dictionary to print to screen"""
    message = ""
    num = 1
    for obstacle in dictionaryList:
        message += "%s. %-20s\n" % (num, obstacle[0])
        num += 1
    parentWindow.withdraw()
    display = SubDisplay(parentWindow, [], button, title=title)
    display.addComponents(
        {
            'element': tkinter.Label(display, anchor=tkinter.W, text=message, justify=tkinter.LEFT, **subScreenProps).pack(side=tkinter.LEFT, expand=tkinter.NO)
        }
    )
