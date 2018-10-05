import threading
from enum import Enum

class ThreadState(Enum):
    NOT_INITIALIZED = 0
    START = 1
    RUNNING = 2
    PAUSED = 3
    END = 4

class Thread(threading.Thread):
    
    '''
    Class name: Thread
    Class Purpose: To handle multiple events
    Inherits: threading.Thread (a class to handle multiple events)
    '''

    def __init__(self, name, priority, callback, args=()):

        '''
        Purpose: To initialize a thread object
        Parameters:
            - name(str): The name of the thread
            - priority (int): The priority of the thread
            - callback (func): The function that will be run from the thread
            - args (tuple): List of arguments for callback function
        
        Returns: None
        '''

        super().__init__(target=callback, name=name, args=args)
        self._name = name
        self._state = ThreadState.NOT_INITIALIZED
        self._priority = priority
        self.callbackFunc = callback

    def __repr__(self):

        """High level repr of thread"""
        return "Thread({0}, {1}, {2})\n".format(
                            self._name, self._priority, self.callbackFunc.__name__ )

    def __str__(self):

        """Easy, user repr. of thread"""
        return "Thread object, with name = {} and callback function = {}\n".format(
                                            self._name, self.callbackFunc.__name_ss_)

    def run(self):

        """Overrides base class"""
        self._state = ThreadState.RUNNING

    def startThread(self):

        """Call the parent start method to run thread"""
        self._state = ThreadState.START
        self.start()

    def pauseThread(self):

        """Pause the thread"""
        self._state = ThreadState.PAUSED

    def joinThread(self, timeout=None):

        """Call the parent join method to join thread"""
        self.join(timeout=timeout)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, newState):
        self._state = newState

    @property
    def priority(self):
        return self._priority

    def isActive(self):

        '''
        Purpose: To determine if the thread is currently running
        Parameters: None
        
        Returns: A boolean to indicate if it is
        '''

        if self._state == ThreadState.RUNNING:
            return True
        return False