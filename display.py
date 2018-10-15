import graphics
from graphics import Image, Point, Rectangle, Entry, Text, color_rgb
from widgets import MyButton, defineProps, defineTextProps, buttonProps
from music import Music
from enum import Enum
from gameplay import *
from threading import Timer
from thread import Thread, Semaphore
import tkinter
import datetime
import time
import sys

# create the semaphore for thread syncing
threadSemaphore = Semaphore()

# decorator to check input values
# acceptable input values is parameter1
# position to place error message is second
def errorCheckText(validValues, position):
    def check(func):
        def wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            errorTextField = None

            # if not valid, print text indicating
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
    PAUSED = 2
    RESULT = 3
    AGAIN = 4
    END = 5

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
            sys.exit()

        def pausePressed():
            self._pauseButton.lastClick = datetime.datetime.now().time()
            self._pauseButton.pressed = not self._pauseButton.pressed
            updateButtonProps = buttonProps
            updateButtonProps['width'] = 22
            updateButtonProps['height'] = 2

            # create a separate display and give properties
            menuDisplay = SubDisplay(self, [], self._pauseButton)
            aboutButton = MyButton(menuDisplay, "About Game", **updateButtonProps)
            aboutButton.config(command=lambda: aboutGame(aboutButton, menuDisplay))
            aboutButton.place(x=0, y=0)
            creatorButton = MyButton(menuDisplay, "About Creator", **updateButtonProps)
            creatorButton.config(command=lambda: aboutCreator(creatorButton, menuDisplay))
            creatorButton.place(x=0, y=50)
            statsButton = MyButton(menuDisplay, "Game Statistics", **updateButtonProps)
            statsButton.config(command=lambda: gameStats(gameInstance, statsButton, menuDisplay))
            statsButton.place(x=0, y=100)
            exitButton = MyButton(menuDisplay, "Exit Screen", **updateButtonProps, command=lambda:menuDisplay._destroyWindow()).place(x=0, y=150)

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

    @property
    def state(self):

        """Getter for the state of the display"""
        return self._dislayState

    @state.setter
    def state(self, newState):

        """Setter for the state of the display"""
        self._dislayState = newState

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
            "You must collect 3 horcruxes in order to win. Let's get started!"
        )
        welcomeMessage = FlashText(self, 
                                   welcomeText, 
                                   Point(rectangleBox.getP1().getX()+15,
                                         rectangleBox.getP1().getY()+15),
                                   0, 50, 7, 15,
                                   textcolor='green')
        text, entry = self._continueMessage(Point((messageBoxTop.getX()+messageBoxBottom.getX())/2-75, 
                                                   messageBoxBottom.getY()-40))
        return rectangleBox, welcomeMessage, text, entry

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
        welcomeBox, \
        welcomeText, \
        continueText, \
        continueField = self._showWelcomeScreen(
                            Point(self.getWidth()/2 - 200, self.getHeight()*3/4 - 100),
                            Point(self.getWidth()/2 + 200, self.getHeight()*3/4 + 100))
        return titleText, welcomeBox, welcomeText, continueText, continueField

    def updateScene(self, gameInstance):

        """Main thread run to update scene of game"""
        
        def changeState(newState):
            
            '''To update the state currently to old state'''
            self._oldState = self._currentState
            self._currentState = newState

        def closeProcess(*deletingObjects):

            '''To close the thread and window, along with cleanup'''
            self._completeFuncAfterTime(4000, self._printGoodbye)
            self._deleteObject(*deletingObjects)
            time.sleep(1)
            changeState(DisplayState.END)
            self.close()

        # Update scene until we are at the end;
        # Initialize all variables needed first;
        # Also, create background, buttons, and copyright
        self._createBackground(Point(self.getWidth()/2, self.getHeight()/2))
        self._createButtons(gameInstance, 'Exit Game', 'Pause Game', 'Pause Music')
        self._showCopyrightMessage(Point(490, 580))

        # start updating screen until the end is reached
        while self._currentState != DisplayState.END:
            # make sure screen is still open
            if self.isClosed():
                sys.exit()

            # check the state and act appropriately
            stateChanged = self._stateChanged()
            if self._currentState == DisplayState.START and not stateChanged:
                titleText, \
                welcomeBox, \
                welcomeText, \
                continueText, \
                continueField = self._initializeDisplay()

                # buttons are initially inactive; activate them
                self._pauseButton.config(state='normal')
                textEntered = self._handleEnterWithText(continueField)
                if textEntered == 'y':
                    self._deleteObject(continueText, continueField, welcomeText)
                    changeState(DisplayState.REGPLAY)
                else:
                    closeProcess(continueText, continueField, welcomeText)    
                
            elif self._currentState == DisplayState.REGPLAY and not stateChanged:
                pass
            elif self._currentState == DisplayState.PAUSED and not stateChanged:
                pass
            elif self._currentState == DisplayState.RESULT and not stateChanged:
                pass
            elif self._currentState == DisplayState.AGAIN and not stateChanged:
                pass

    def _printGoodbye(self):

        """Print a goodbye message on screen with properties"""
        goodbye = FlashText(
                        self,
                        "GOODBYE AND HAVE A NICE DAY!",
                        Point(125, 400),
                        0, 24, 15, 20,
                        textcolor='green', size=20
                    )
        return goodbye

    def _continueMessage(self, locationStart):

        """Function to print if the user wish to continue and validates input
            - locationStart (point): Where the message will start"""
        
        textField = Text(locationStart, "Do you wish to continue? (y/n)")
        defineTextProps(textField, textcolor='green')
        textField.draw(self)
        entryField = Entry(Point(locationStart.getX()+150, 
                                 locationStart.getY()), 15)
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

    @errorCheckText(['y', 'n'], Point(300, 535))
    def _handleEnterWithText(self, textField):

        """Wait for user to press Enter key,
           then print appropriate message"""

        key = ''
        while key != 'Return':
            try:
                key = self.getKey()
            except:
                sys.exit()
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
                sys.exit()
            self._characters.append(textElement)
            currentPosition = Point(currentPosition.getX()+spaceX, currentPosition.getY())
            currentCharNum = currentCharNum + 1
            time.sleep(self._delay)

    def undraw(self):

        """Undraw the objects"""
        for character in self._characters:
            character.undraw()

subScreenProps = {
    'foreground': 'green',
    'background': 'black'
}

def aboutGame(button, parentWindow):

    """Display information about the game"""
    gameInfo = (
        "\n\nThe Search For Horcruxes is a text based game that is based on\n"
        "the 'Harry Potter' movies. The game is won by finding 3 Horcruxes.\n"
        "A horcrux is an item that holds Lord Voldemort's (Harry's nemesis) soul.\n"
        "You have ten moves to find these horcruxes, but will find this difficult, as\n"
        "you will face Voldemort's followers. This a fun game for Pottermores!\n\n\n"
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
        "\n\WINS: {}\n\n"
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