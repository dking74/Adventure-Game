import random

goodCharacters = [
    "Harry",
    "Hermione",
    "Ron",
    "Sirius",
    "Professor Dumbledore",
    "Ginny",
    "Fred",
    "George",
    "Nevil",
    "Luna",
    "Professor McGonnagal",
    "Remus",
    "Tonks",
    "Dobby"
]

# lists for ranges of power for enemy key attributes
MOST_POWERFUL = [80, 100]
POWERFUL = [60, 100]
SKILLED = [40, 60]
AVERAGE = [20, 40]
WEAK = [0, 20]

def generateEnemyStats(healthRange, powerRange):
    """A function to generate stats for an enemy"""

    stats = {
        'healthRating': random.randint(healthRange[0], healthRange[1]),
        'powerRating': random.randint(powerRange[0], powerRange[1]),
        'health': 100
    }
    return stats

enemies = [
    {"Voldemort": generateEnemyStats(MOST_POWERFUL, MOST_POWERFUL)},
    {"Draco": generateEnemyStats(AVERAGE, SKILLED)},
    {"Crabbe": generateEnemyStats(WEAK, AVERAGE)},
    {"Goyle": generateEnemyStats(WEAK, WEAK)},
    {"Bellatrix": generateEnemyStats(POWERFUL, POWERFUL)},
    {"Lucious": generateEnemyStats(SKILLED, POWERFUL)},
    {"Narcissa": generateEnemyStats(AVERAGE, SKILLED)},
    {"Grindelwald": generateEnemyStats(POWERFUL, MOST_POWERFUL)},
    {"Pius": generateEnemyStats(SKILLED, SKILLED)},
    {"Snape": generateEnemyStats(SKILLED, POWERFUL)},
    {"Dolores": generateEnemyStats(AVERAGE, SKILLED)},
    {"Greyback": generateEnemyStats(SKILLED, POWERFUL)},
    {"Barty Crouch": generateEnemyStats(SKILLED, POWERFUL)},
    {"Carrow": generateEnemyStats(POWERFUL, SKILLED)},
    {"Yaxley": generateEnemyStats(POWERFUL, POWERFUL)},
    {"Professor Quirrel": generateEnemyStats(SKILLED, AVERAGE)},
    {"Salazar Slyerin": generateEnemyStats(MOST_POWERFUL, MOST_POWERFUL)}
]