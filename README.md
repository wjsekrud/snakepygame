## A Simple Snake Game
This is a simple snake game, an example of pygame utilization.

## Game rule
1. The player is green snake. The snake always moves forward for each frame, and you can steer its direction with arrows.
2. Orange colored box is the feed. If your snake eats the feed by moving onto it, your snake will gain length by one, and the speed will be increased in certain amount.
3. On every time the snake eat feed, a random grey obstacle spawns on random rocation on the map. The number of obstacles is accmulative according to the total amount of the feeds you ate.
4. If the snake goes out of the bound, or hits an obstacle or itself, the game is over.
5. There also is a snake bot chasing for feed. You can Kill it by blocking its path. Can respawn

The feeds give you 100 scores each, but start to rot as time passes. 10 points decrease per every 10 ticks. 
A special blue feed rarely spawns. It removes all obstacles when eaten, but does not provide any scores.

When you hit LCTRL in the results screen, autoplay starts.

Arcade font from (https://www.dafont.com/arcade-ya.font)
