# Resurgence-From-Ruin
A 2D video game with 5 increasingly challenging levels involving enemy battles, a maze to collect gemstones, and a shop to buy weapons. 
### Overview
I created a game in Python using Pygame. The aim is to collect gemstones from a maze to earn money, buy weapons from the shop that can then be stored in the player inventory, and use these weapons to battle enemies across 5 levels that increase in difficulty. Every time a player wins a level, they progress to the next one, and if they complete all of them, they win the entire game. Conversely, every time they lost a battle, their damage score is incremented, and if it exceeds 5, they lose the entire game. As many games are either too long to play in one sitting or too short and repetitive to occupy a player for long, I sought to create a game that would achieve the best of both worlds. 

### Features and Highlights
#### Gameplay features
- An in-game menu with 4 buttons to navigate to the main 4 game states (maze, battle, shop or progress tracker). Across the entire game, buttons are incorporated for intuitive navigation to different parts of the game
- A maze which the user must navigate to collect gemstones that increase their money count. It can be played as many times as desirable, and each time, the particular design of the maze and number of gemstones will vary
- 5 levels, each with a different background and obstacle theme. Obstacles make the game more engaging as they can be used to hide behind, and can impede shots by either the player or enemies
- 4 different types of enemy, with 2 contact-only (short-range) enemies and 2 long-range enemies (which attack the player from a distance by firing at them). The first 4 levels feature 10 enemies, 5 of each type. The final level is of extra difficulty, as it has 2 extra enemy types, and a total of 20 enemies to defeat. On each level, the damage that can be done by an enemy increases, thus each level is harder than the previous one
- A health bar displayed during battles, so the player can see how much of their health remains. If health is low, it will turn from green to red as a warning
- A shop where weapons can be bought and are added to the player's inventory if they have sufficient money. Any items that are too expensive for the player are indicated as such and an error sound will play if the user attempts to purchase them
- 6 different weapons, including 3 short-range and 3 long-range weapons. The long-range ones fire projectiles such as bullets to attack an enemy at a distance
- A progress tracker displaying the user's level and damage score which dynamically updates every time a battle is played
- Includes high-quality assets (graphics and sounds) sourced from OpenGameArt, to enhance gameplay

#### Technical features
- Object-oriented architecture implemented consistently to ensure modular and scalable design of the game, with classes being used to define attributes and methods of all major entities such as the sprite, enemies, gemstones, weapons and projectiles
- Custom inventory system designed as a class. Each slot is represented with an attribute, storing a list of relevant data (0 or 1 to indicate if the slot is filled, and the item itself, or None if containing no item). I designed several methods to handle the inventory, including a method to fill an inventory slot (after purchasing a weapon) and a method to select and highlight any slot in the inventory (during battle)
- Pixel-perfect collision detection using image masks
- Animation when player uses a sword, through repeatedly rendering and rotating slightly the weapon image
- Fully-developed short-range enemy navigation in battles. The distance between the player and enemy is used to calculate the unit vector, and the enemy moves in this direction to pursue the player. In order to bypass an obstacle it collides with, the enemy's direction is temporarily diverted using a randomly selected unit vector to prevent getting stuck
- Projectile system where players or long-range enemies may fire objects at other entities to deplete health points, with unit vector calculations also being utilised for this. Projectiles originating from long-range enemies have randomised timers to add variability to the game
- Dynamic shop interface, where it is clearly indicated whether an item is available to be bought, is too expensive to be bought, or can no longer be purchased as it has been already. Items added to the inventory are directly usable in the battle game state
- Implementation of entity management by integrating lists throughout the game, including for tracking inactive and active projectiles, and tracking gemstones in the maze yet to be collected
  

## Getting Started

### Prerequisites
- Python 3.13.7+ (earlier versions should work, but I have not tested them)
- pip (Python package manager needed to download the requirements
- Python package requirements as outlined in requirements.txt

### Installation
1. Clone the repo:
````
git clone https://github.com/github_username/repo_name.git
````
2. Install dependencies
````
pip install -r requirements.txt
````
3. Once dependencies are installed and the repository has been cloned, run in the command line:
````
python src/main.py
````
