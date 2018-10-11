import threading
from enum import Enum

class Thread(threading.Thread):
    
    '''
    Class name: Thread
    Class Purpose: To handle multiple events
    Inherits: threading.Thread (a class to handle multiple events)
    '''

    def __init__(self, name, priority, callback, *args):

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
        self._priority = priority
        self.callbackFunc = callback

    def __repr__(self):

        """High level repr of thread"""
        return "Thread({0}, {1}, {2})\n".format(
                            self._name, self._priority, self.callbackFunc.__name__)

    def __str__(self):

        """Easy, user repr. of thread"""
        return "Thread object, with name = {} and callback function = {}\n".format(
                                            self._name, self.callbackFunc.__name__)

    def startThread(self):

        """Call the parent start method to run thread"""
        self.start()

    def joinThread(self, timeout=None):

        """Call the parent join method to join thread"""
        self.join(timeout=timeout)

class Semaphore(threading.Semaphore):
    """A class with the ability to lock threads"""

    def __init__(self):
        pass