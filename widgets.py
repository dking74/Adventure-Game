from tkinter import Button, Label
from enum import Enum
import graphics

#properties of a general button
buttonProps = {
    'highlightthickness': '2px',  
    'width': 9, 
    'height': 2,
    'relief': 'raised'
}

class ButtonState(Enum):
    NOTPRESSED = 0
    PRESSED = 1

class MyLabel(Label):
    """Label widget class"""

    def __init__(self, mainWindow, labelName="", **props):
        """Initialization of label
            mainWindow (GraphWin): The parent object to add to
            labelName (Str): The text to give label
            props (dict): Props to give label"""

        super().__init__(mainWindow, text=labelName, **props)
        self._labelName = labelName
        self._props = props

    def __str__(self):
    
        """print string representation of object"""
        return "{} object with name '{}'".format(
                    self.__class__.__name__, self._labelName)

    @property
    def labelName(self):

        """Get the label name"""
        return self._labelName

    @labelName.setter
    def labelName(self, newName):

        """Set the new label name"""
        self._labelName = newName

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
        
        """Change the config to state of normal"""
        self.config(state='normal')

    def disableButton(self):

        """Change the config to state of disabled"""
        self.config(state='disabled')

def defineProps(drawObject, **props):

    """Initialize properties of widget or shape"""
    try:
        drawObject.setFill(props.get('fill', ''))
        drawObject.setOutline(props.get('outcolor', 'black'))
        drawObject.setWidth(props.get('outwidth', 1))
    except (graphics.GraphicsError, AttributeError):
        pass

def defineTextProps(drawObject, **props):

    """Properties for text fields"""
    try:
        drawObject.setTextColor(props.get('textcolor', 'black'))
        drawObject.setStyle(props.get('style', 'normal'))
        drawObject.setFace(props.get('face', 'helvetica'))
        drawObject.setSize(props.get('size', 12))
    except (graphics.GraphicsError, AttributeError) as detail:
        print(detail)