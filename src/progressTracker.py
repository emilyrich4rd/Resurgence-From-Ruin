# file for progress tracker code 

import pygame
pygame.init()

# importing other files here
from gameData import * 
from shop import * # so I can borrow the shop button to go back to main menu
from imageData import *

def drawBars(): # sets up the rectangle templates for layering levels/damage score on top
    levelBar = pygame.Rect(dimensions[0]*resolution*0.2, dimensions[1]*resolution*0.3, 500, 80)
    damageScoreBar = pygame.Rect(dimensions[0]*resolution*0.2, dimensions[1]*resolution*0.6, 500, 80)
    pygame.draw.rect(display, 'grey', levelBar)
    pygame.draw.rect(display, 'grey', damageScoreBar)

def setLabels(): # labels to annotate one bar as 'level' and one bar as 'damage'
    display.blit(levelImg, (dimensions[0]*resolution*0.2, dimensions[0]*resolution*0.18))
    display.blit(damageImg, ((dimensions[0]*resolution*0.2, dimensions[0]*resolution*0.42)))

font = pygame.font.Font('freesansbold.ttf', 32) # sets the font for the level or damage score, which will also be written as a number

def writeLevel(level): # writes the level num onto screen
    levelText = font.render(str(level), True, (255,255,255)) # sets the desired text in the appropriate font and colour
    levelTextRect = levelText.get_rect() # text can be referred to as a rectangle object in this way
    levelTextRect.center = (dimensions[0]*resolution*0.7, dimensions[1]*resolution*0.44) # centers text
    display.blit(levelText, levelTextRect)
   
def writeDamage(damageScore): # writes the damage score value onto screen
    damageText = font.render(str(damageScore), True, (255,255,255)) # sets the desired text in the appropriate font and colour
    damageTextRect = damageText.get_rect() # text can be referred to as a rectangle object in this way
    damageTextRect.center = (dimensions[0]*resolution*0.7, dimensions[1]*resolution*0.74) # centers text
    display.blit(damageText, damageTextRect)

# 440/5 (88) is the length of one rect
def drawLevel(level): # draws blue bar showing how many levels are complete graphically
    x = (dimensions[0]*resolution*0.2) + 30
    y = (dimensions[1]*resolution*0.3) + 20
    levelRect = pygame.Rect(x, y, 88, 40)
    for i in range(level):
        pygame.draw.rect(display, 'deepskyblue', levelRect)
        x += 88 
        levelRect = pygame.Rect(x, y, 88, 40) # new rect created with the updated x value

def drawDamage(damageScore): # draws blue bar showing damage score graphically
    x = (dimensions[0]*resolution*0.2) + 30
    y = (dimensions[1]*resolution*0.6) + 20
    damageRect = pygame.Rect(x, y, 88, 40)
    for i in range(damageScore):
        pygame.draw.rect(display, 'deepskyblue', damageRect)
        x += 88
        damageRect = pygame.Rect(x, y, 88, 40) # new rect created with the updated x value

def drawProgressTracker(level, damageScore): # wraps related subroutines into one for convenience
    display.fill('mediumslateblue')
    drawBars()
    setLabels()
    drawLevel(level)
    drawDamage(damageScore)
    writeLevel(level)
    writeDamage(damageScore)
    backButton.renderButton()
    pygame.display.flip()





