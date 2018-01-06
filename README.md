# Adventure Game Project

The Adventure Game Project is your one, and only, programming assignment that will stretch across multiple modules and weeks. It will be due in the final week of the course, but is expected that you will start designing and building before the final week.

At this moment you have built enough knowledge and experience to begin conceptualizing elements of your Adventure Game. You will find that concepts yet to come (e.g, classes) can be very helpful in organizing how you implement your final version of this project and it is strongly suggested you integrate them into your design. We are providing this assignment earlier to give you more time to conceive what you want to do and start laying the groundwork for how you want to do it.

 

## Overview
You are to write a text-based adventure game. Generally, in a text-based adventure game, the game outputs some description of a situation you are in and then gives you some options about what to do. For example:

```
You are in a dark hallway and see a treasure chest just 10 steps in front of you.
Only 10 steps left. Step forward (y/n)? y
You found 78 gold pieces! Now you have 78 gold pieces.
```

As you make choices in the game you progress towards some goal. However, as your make progress, there can be impediments along your way (e.g, enemies that "attack" you and deter you on your quest). A player will "win" your game if they can achieve the goal, and lose if the impediments stop them before they reach the goal.

 

## Game Play
As an adventurer, you will be concerned with three things: (1) reaching some stated goal, (2) collecting some random trinket (e.g., gold pieces), and (3) protecting some personal resource (e.g., keeping a health level above 0).

Your game must have the adventurer progress towards some goal (e.g., get to a treasure chest), within 10 "steps" (e.g., step to the treasure chest) by making choices. As progress is made though there should always be at least two possible outcomes: you find a random amount of the trinket or you are confronted by an enemy. It's your game, so you can add more possible outcomes, but those two are required.
```
You are in a dark hallway and see a treasure chest just 10 steps in front of you.
Only 10 steps left. Step forward (y/n)? y
You found 78 gold pieces! Now you have 78 gold pieces.
```
```
Only 8 steps left. Step forward (y/n)? y
An enemy approaches!
It's Aaron Burr! He'll kill your political aspirations and then shoot you in the back!
```

Enemies in the game should have some notion of their own personal resource (e.g., a health level) and a mechanism to deplete your personal resource (e.g., attacking). If you are confronted by an enemy, then you will "attack" the enemy by depleting a random amount of their personal resource. After you "attack", assuming the enemy has any of their personal resource, then they should "attack" you and deplete your personal resource.

```
Attacking Aaron Burr!
Aaron Burr loses 6 health points. 28 health points left.
Aaron Burr is attacking Paul!
You lost 6 health points. 88 health points left.
```

The confrontation ends when either you, the adventurer, or the enemy, has their personal resource reduced to 0 or less. If the adventurer's personal resource is reduced to 0, then the game is over.

If your adventurer should make it all the way to the end, they should receive some "congratulatory" message and a summary of their final statistics: how many of the trinket the collected and how much of their personal resource remains.

```
You reached the treasure chest!
An inside you found... spiders that spin a web to hold you in the hallway for all eternity. :(
GAME OVER

End Health: 45
End Gold: 567
``` 

## Requirements
This is a very open-ended problem and intentionally so. The goal is for you to make design choices about how the game plays, how it is themed, and how you structure the data required to make it work. You are encouraged to be as creative as possible in making your adventure game fun and interesting, the theme is entirely up to you. However, you must adhere to a few requirements:

* Your adventurer must have a name, keep track of how many trinkets they've collected, and their personal resource. They can have other things as well, but these are required.
  * Trinket examples from previous games: Eggo waffles, holiday gifts, and Subway endorsement checks.
  * Personal resouce examples from previous games: time to work on programming assignments, health points, and time for preparing dinner.
* Your enemies must have a name, an introduction (e.g. "It's Aaron Burr! He'll kill your political aspirations and then shoot you in the back!"), and a personal resource that you can reduce when "attacking". Again, other things are also possible and encouraged, but these are required.
  * Enemy examples from previous games: sharks, nosy neighbors, Krampus, and Kylo Ren which had various means of reducing a personal resource beyond "attacking"
* Your adventurer must progress towards something in a 'straight line' (no mazes), no more than 10 steps/moves/transitions/time slices away from the start.
* With each step of progress, it must be possible for the adventurer to collect some amount of your chosen random trinket, or be attacked. Other things can happen as well, but those two must be possible.
* There must be at least three possible enemies you encounter. You should be using some element of random chance so it is possible that on a particular play of the game we might not encounter one or more of the enemies, but there should be at least three possibilities.
* The game must end. It cannot be infinite. Your adventurer may make it to the goal or not make it to the goal, but the game must end at some point without errors (i.e., no Exceptions from Python to end the game).
* Once the game is over, you must at least output the total number of your chosen trinkets the adventurer collected and the final amount of their personal resource. You can output other things as well as they are relevant to your adventure game, but trinket count and personal resource amount are required.
 
## Extra Credit
Within this assignment extra credit is possible at the discretion of the instructor. Students who go above and beyond the requirements (e.g., adding other interesting possible outcomes to taking a step, a clever theme that required extra effort, other creative features) may be awarded extra credit points.

In order to eligible for extra credit you will need to provide documentation for any effort you feel is above and beyond. You should do so both in your program code with comments as well as in this Canvas submission, as indicated by the last questions in the Canvas Submission section.
