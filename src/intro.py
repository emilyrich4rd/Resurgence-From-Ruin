# file for code relating to set-up of the game; the start screen, backstory screen (describing how to play the game) and in-game menu

import pygame
pygame.init()
from gameData import * 
from imageData import *

# general function to set background
def setBG(img):
    display.blit(img, (0,0))


# button to start the game; buttonScalerX and buttonScalerY are defined in gameData.py
startButton = Button(maxX*0.4, maxY*0.7, buttonScalerX, buttonScalerY, startGameImg, startHoverImg)

# sets the game starting screen - buttons and background image 
def runStartScreen(img, button):
    setBG(img)
    button.renderButton()
    pygame.display.flip()

# button for transitioning from screen explaining how to play the game to the in-game menu
goToMenu = Button(maxX*0.4, maxY*0.8, buttonScalerX, buttonScalerY, goToMenuImg, goToMenuHover) # actual instantiation of button

# summarises the rendering of the backstory screen into one function
def setBackstory(img, button):
    setBG(img)
    button.renderButton()
    pygame.display.flip()

# instantiation of shop button 
b1X = (resolution * dimensions[0])*0.36
b1Y = (resolution * dimensions[1])*0.65
shopButton = Button(b1X, b1Y, 300, 150, shopButtonImg, shopButtonHoverImg)

# instantiation of maze button
b2X = (resolution * dimensions[0])*0.15
b2Y = (resolution * dimensions[1])*0.4
mazeButton = Button(b2X, b2Y, 300, 150, mazeButtonImg, mazeButtonHoverImg)

# instantiation of progress tracker button
b3X = (resolution * dimensions[0])*0.36
b3Y = (resolution * dimensions[1])*0.22
progressTrackerButton = Button(b3X, b3Y, 300, 150, progressTrackerButtonImg, progressTrackerButtonHoverImg)

# instantiation of battle button
b4X = (resolution * dimensions[0])*0.56
b4Y = (resolution * dimensions[1])*0.4
battleButton = Button(b4X, b4Y, 300, 150, battleButtonImg, battleButtonHoverImg)


# shows menu and all navigation buttons
def renderMenu(img, b1, b2, b3, b4): #b1 to 4 are the relevant buttons, while img will allow me to display the in-game menu image
    setBG(img)
    moneyCount.renderMoney()
    b1.renderButton()
    b2.renderButton()
    b3.renderButton()
    b4.renderButton()
    pygame.display.flip()


