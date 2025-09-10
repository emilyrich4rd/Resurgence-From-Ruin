# file for loading all sounds from the 'sounds' file into the game

import pygame
pygame.init()
pygame.mixer.init() # initialises the mixer, which handles sound effects
import os # for file handling to load images 

sounds = 'sounds' # directory name

# loading sounds from directory into main game
gemCollectedSound = pygame.mixer.Sound(os.path.join(sounds, 'coin.flac'))
mazeCompleteSound = pygame.mixer.Sound(os.path.join(sounds, 'Rise03.mp3'))
itemBoughtSound = pygame.mixer.Sound(os.path.join(sounds, 'coinsplash.ogg'))
failedPurchaseSound = pygame.mixer.Sound(os.path.join(sounds, 'error.ogg'))
weaponSound = pygame.mixer.Sound(os.path.join(sounds, 'Bow.wav'))
playerHitSound = pygame.mixer.Sound(os.path.join(sounds, 'Relic Attack 5.mp3'))
enemyHitSound = pygame.mixer.Sound(os.path.join(sounds, 'impact.1.ogg'))
battleLostSound = pygame.mixer.Sound(os.path.join(sounds, 'game_over_bad_chest.wav'))
battleWonSound = pygame.mixer.Sound(os.path.join(sounds, 'Win sound.wav'))
gameWonSound = pygame.mixer.Sound(os.path.join(sounds, 'killvictory1.mp3'))
gameLostSound = pygame.mixer.Sound(os.path.join(sounds, 'Icy Game Over.mp3'))
clickSound = pygame.mixer.Sound(os.path.join(sounds, 'sound_click.wav'))


