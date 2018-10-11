from tkinter import Button
from enum import Enum
import graphics

class ButtonState(Enum):
    NOTPRESSED = 0
    PRESSED = 1

class MyButton(Button):
    """Button widget class"""

    def __init__(self, mainWindow, buttonName="", **props):
        """Initialization of button
            mainWindow (GraphWin): The parent object to add to
            buttonName (Str): The text to give button
            props (dict): Props to give button"""
        

        super().__init__(mainWindow, text=buttonName, **props)
        self._buttonName = buttonName
        self._lastClick = None
        self._callbackFunc = None
        self._props = props
        self.pressed = ButtonState.NOTPRESSED

    def __str__(self):

        """print string representation of object"""
        return "{} object with name '{}'".format(
                    self.__class__.__name__, self._buttonName)

    @property
    def buttonName(self):

        """Return the button name"""
        return self._buttonName

    @buttonName.setter
    def buttonName(self, newName):

        """Sets the new button name"""
        self.config(text=newName)
        self._buttonName = newName

    @property
    def lastClick(self):

        """Return the last click for button"""
        return self._lastClick
        
    @lastClick.setter
    def lastClick(self, newClick):

        """Set new last click for button"""
        self._lastClick = newClick

    @property
    def callbackFunc(self):

        """Return callback func name"""
        return self._callbackFunc

    @callbackFunc.setter
    def callbackFunc(self, newCallback):

        """set new callback function"""
        self._callbackFunc = newCallback
        self.config(command=self._callbackFunc)

    def enableButton(self):
        pass

    def disableButton(self):
        pass

def defineProps(drawObject, **props):

    """Initialize properties of widget or shape"""
    try:
        drawObject.setFill(props.get('fill', ''))
        drawObject.setOutline(props.get('outcolor', 'black'))
        drawObject.setWidth(props.get('outwidth', '1'))
        drawObject.setStyle(props.get('style', 'normal'))
        drawObject.setFace(props.get('face', 'helvetica'))
        drawObject.setSize(props.get('size', '12'))
        drawObject.setTextColor(props.get('textcolor', 'black'))
    except (graphics.GraphicsError, AttributeError):
        pass
