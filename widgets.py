from tkinter import Button
from enum import Enum

class ButtonState(Enum):
    NOTPRESSED = 0
    PRESSED = 1

class MyButton(Button):
    """Button widget class"""

    def __init__(self, mainWindow, callback, buttonName="", *args, **props):
        """Initialization of button
            mainWindow (GraphWin): The parent object to add to
            callback (Func): Callback function to happen when button is pressed
            buttonName (Str): The text to give button
            props (dict): Props to give button
            args (list): Arguments for callback func"""
        

        super().__init__(mainWindow, text=buttonName, 
                         width=props['width'] if 'width' in props else None,
                         height=props['height'] if 'height' in props else None,
                         command=lambda: callback(*args))
        self._callbackFunc = callback
        self._buttonName = buttonName
        self._lastClick = None
        self._props = props
        self.pressed = ButtonState.NOTPRESSED

    def packButton(self):

        """Function to place button on window"""
        # self.pack(side=self._props['side'] if 'side' in self._props else None,
        #            padx=self._props['padx'] if 'padx' in self._props else None,
        #            pady=self._props['pady'] if 'pady' in self._props else None)

        
        self.grid(row=0,column=1)
                  #padx=self._props['padx'] if 'padx' in self._props else None,
                  #pady=self._props['pady'] if 'pady' in self._props else None)
        print (self.grid_size())

    def __str__(self):

        """print string representation of object"""
        return "{} object with name '{}' and callback function '{}'".format(
                    self.__class__.__name__, self._buttonName, self._callbackFunc.__name__)

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
        return self._callbackFunc.__name__

    @callbackFunc.setter
    def callbackFunc(self, newCallback):

        """set new callback function"""
        self._callbackFunc = newCallback
        self.config(command=self._callbackFunc)