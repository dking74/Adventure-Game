from enum import Enum

class MusicState(Enum):
    STARTED = 0
    PLAYING = 1
    PAUSED = 2
    STOPPED = 3

class Music():
    """Class to play music for application"""

    def __init__(self, themesong):

        """initialize theme song instance"""
        self._themesong = themesong
        self._state = MusicState.STARTED

    def _installPyGame(self):
          
        """Function to install Pygame if not already installed"""
        try:
            import pygame
        except ImportError:    
            import os
            osCall = os.system('pip3 install pygame')
            if osCall != 0:
                osCall = os.system('pip install pygame')
                if osCall != 0:
                    return False
        return True

    def _initializeMusic(self):

        """Initialize the music player"""
        pygame.mixer.init()

    def _loadMusic(self):

        """Load the current music file"""
        pygame.mixer.music.load(self._themesong)

    def _playMusic(self, times):

        """Play the current music a set amount of times"""
        pygame.mixer.music.play(times)

    def _currentlyPlaying(self):

        """Check if the music is currently playing"""
        return pygame.mixer.music.get_busy()

    def playThemeMusic(self, displayInstance):

        '''
        Purpose: Play theme music in background
        Parameters:
            - displayInstance (MainDisplay): The display instance to track
        
        Returns: None
        '''

        # determine if py game is installed, if not install it
        installed = self._installPyGame()
        if installed:

            # globally import pygame to use in other helper functions
            global pygame
            import pygame

            # initialize music and start music player
            self._initializeMusic()
            self._state = MusicState.STARTED
            currentlyPlaying = self._currentlyPlaying()
            if not currentlyPlaying:
                self._loadMusic()
                self._playMusic(-1)
            else: 
                pass
        else:
            print("Could not install pygame...No music")

    @staticmethod
    def pauseMusic():

        """Pause the music from playing"""
        pygame.mixer.music.pause()

    @staticmethod
    def resumeMusic():

        """Resume the music from pause"""
        pygame.mixer.music.unpause()

    