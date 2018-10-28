import random

# lists for ranges of power for enemy key attributes
MOST_POWERFUL = 5
POWERFUL = 4
SKILLED = 3
AVERAGE = 2
WEAK = 1

def generateEnemyStats(healthRange, powerRange, smartsRating):
    """A function to generate stats for an enemy"""

    stats = {
        'healthRating': healthRange,
        'powerRating': powerRange,
        'smartsRating': smartsRating
    }
    return stats

enemies = {
    "Voldemort": generateEnemyStats(MOST_POWERFUL*20, MOST_POWERFUL, POWERFUL),
    "Draco": generateEnemyStats(AVERAGE*20, SKILLED, SKILLED),
    "Crabbe": generateEnemyStats(WEAK*20, AVERAGE, AVERAGE),
    "Goyle": generateEnemyStats(WEAK*20, WEAK, WEAK),
    "Bellatrix": generateEnemyStats(POWERFUL*20, POWERFUL, POWERFUL),
    "Lucious": generateEnemyStats(SKILLED*20, POWERFUL, SKILLED),
    "Narcissa": generateEnemyStats(AVERAGE*20, SKILLED, POWERFUL),
    "Grindelwald": generateEnemyStats(POWERFUL*20, MOST_POWERFUL, POWERFUL),
    "Pius": generateEnemyStats(SKILLED*20, SKILLED, AVERAGE),
    "Snape": generateEnemyStats(SKILLED*20, POWERFUL, MOST_POWERFUL),
    "Dolores": generateEnemyStats(AVERAGE*20, SKILLED, SKILLED),
    "Greyback": generateEnemyStats(SKILLED*20, POWERFUL, SKILLED),
    "Carrow": generateEnemyStats(POWERFUL*20, SKILLED, AVERAGE),
    "Yaxley": generateEnemyStats(POWERFUL*20, POWERFUL, AVERAGE),
    "Professor Quirrel": generateEnemyStats(SKILLED*20, AVERAGE, AVERAGE),
    "Salazar Slytherin": generateEnemyStats(MOST_POWERFUL*20, MOST_POWERFUL, POWERFUL)
}

class Character():
    
    """Class to handle character attributes"""
    def __init__(self):
        self._characterName = ""
        self._characterStrength = ""
        self.characterHealth = 75
        self.characterPower = 5
        self.characterSmarts = 5

    @property
    def strength(self):

        """Get the character strength"""
        return self._characterStrength

    @strength.setter
    def strength(self, strength):

        """Set the character strength"""
        self._characterStrength = intToStrength[strength]
        if self._characterStrength == 'Health': self.characterHealth = 100
        elif self._characterStrength == 'Power': self.characterPower = 15
        elif self._characterStrength == 'Smarts': self.characterSmarts = 20

    @property
    def characterName(self):

        """Getter to get the current character name"""
        return self._characterName

    @characterName.setter
    def characterName(self, characterName):

        """A setter to set the character name"""
        self._characterName = characterName

# dictionary to convert number to strength
intToStrength = {
    '1': 'Health',
    '2': 'Power',
    '3': 'Smarts'
}