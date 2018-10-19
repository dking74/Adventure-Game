from thread import threadSemaphore
import random
import time

class Fight():
    """Class to simulate a fight with enemy"""

    def __init__(self, enemy, enemyStats, character):
        
        """Initialize a fighting instance with the enemy"""
        self._fightMessage = None
        self._enemy = enemy
        self._enemyStats = enemyStats
        self._fightOn = True
        self._fightMessage = ""
        self._fightResult = ""
        self._player = character.characterName
        self._playerStats = dict(healthRating=character.characterHealth,
                                 powerRating=character.characterPower,
                                 smartsRating=character.characterSmarts)

    @property
    def fightOn(self):

        """Getter for determining if fight is happening"""
        return self._fightOn

    @fightOn.setter
    def fightOn(self, newStatus):

        """Setter for changing status of fight"""
        self._fightOn = newStatus

    @property
    def fightMessage(self):

        """Getter for the current fight message"""
        return self._fightMessage

    @property
    def fightResult(self):

        """Getter to determine the fight result"""
        return self._fightResult

    def _getFightMove(self, spellCaster):

        """Function to generate a random move
           that is made by user"""
        spellInfo = random.choice(spells)
        spellCasted = list(spellInfo.keys())[0]
        spellDamage = list(spellInfo.values())[0]
        spellHit = random.choice(spellResult)
        overallDamage = 0
        healthLeft = 0
        spellReceiver = ""

        # determine if the spell hit 
        hit = False
        if spellHit == 'hit':
            hit = True

        # determine who loses points
        if spellCaster == self._player:
            spellReceiver = self._enemy
            if hit: 
                overallDamage = self._playerStats['powerRating'] * spellDamage
                self._enemyStats['healthRating'] = self._enemyStats['healthRating'] - overallDamage
                healthLeft = self._enemyStats['healthRating']
        else:
            spellReceiver = self._player
            if hit: 
                overallDamage = self._enemyStats['powerRating'] * spellDamage
                self._playerStats['healthRating'] = self._playerStats['healthRating'] - overallDamage
                healthLeft = self._playerStats['healthRating'] 

        print(overallDamage)

        if healthLeft < 0: healthLeft = 0
        self._fightMessage = (
            "{} casted a {} spell. The result was a {}. ".format(spellCaster, spellCasted, spellHit)
        )
        addedMessage = "{} points in damage was done and {} has {} health points left.".format(overallDamage, spellReceiver, healthLeft) if spellHit == 'hit' else \
                       "No damage was done to {}".format(spellReceiver)
        self._fightMessage = self._fightMessage + addedMessage
                    
    def _determineFightResult(self):

        """Determine who won the fight and next steps"""
        self._fightOn = False
        if self._playerStats['healthRating'] <= 0:
            self._fightResult = 'lose'
        elif self._enemyStats['healthRating'] <= 0:
            self._fightResult = 'win'
        else:
            self._fightResult = 'tie'        

    def fight(self):
        
        """Function to simulate a fight
           between the current character and enemy"""
        moves = 1
        firstMove = True
        fightMoves = 5
        while fightMoves > 0 and self._enemyStats['healthRating'] > 0 and self._playerStats['healthRating'] > 0:
        
            print(self._playerStats)
            if firstMove:
                firstMove = False
            else:
                threadSemaphore.lock()
            self._getFightMove(self._player)
            threadSemaphore.unlock()
            time.sleep(.3)
            threadSemaphore.lock()
            print(self._enemyStats)
            self._getFightMove(self._enemy)
            fightMoves = fightMoves - 1
            threadSemaphore.unlock()
            time.sleep(.3)
            moves = moves + 1

        # get the result of the fight
        threadSemaphore.lock()
        self._determineFightResult()

# spell ratings
spells = [
    {'Crucio': 15},
    {'Imperio': 8},
    {'Expelliarmus': 6},
    {'Stupefy': 3},
    {'Impedimenta': 7},
    {'Protego': 8},
    {'Obliviate': 4},
    {'Expecto Patronum': 9},
    {'Confundo': 6},
    {'Sectumsempra': 10},
    {'Incendio': 7},
    {'Diffendo': 5},
    {'Relashio': 9},
    {'Confringo': 7},
    {'Everte Statum': 3},
    {'Fiendfyre': 6},
    {'Impervius': 8},
    {'Incendio': 2},
    {'Obliviate': 7},
    {'Petrificus Totalus': 3},
    {'Repello Inimicum': 7},
    {'Serpensortia': 5},
    {'Titillando': 3},
    {'Wingardium Leviosa': 5},
    {'Aquamenti': 6},
    {'Reducto': 7},
    {'Expulso': 6},
    {'Incarcerous': 5},
    {'Transmogrify': 8},
    {'Legilimens': 6},
    {'Avada Kedavra': 20}
]

spellResult = [
    'hit',
    'miss'
]
