# file for loading all images from the 'images' file into the game

import pygame
pygame.init()
import os
imageFolder = 'images' # name of directory where images are stored

# defining the pygame window/screen 
resolution = 32 # number of pixels per unit of the screen
dimensions = (30, 24) # a tuple for the number of units in the x and y axis respectively 
screen = (dimensions[0] * resolution, dimensions[1] * resolution) # sets the window size
myScreen = pygame.display # creates a display Surface
display = myScreen.set_mode(screen) # initialises display screen
myScreen.set_caption('Resurgence From Ruin') # name of my window 

# maze background 
mazeBackgroundImg = pygame.image.load(os.path.join(imageFolder,'retroSunset.png'))
mazeBackgroundImg = pygame.transform.scale(mazeBackgroundImg, (dimensions[0]*resolution, dimensions[1]*resolution))

# gemstones
scaleSize = 30
quartzImg = pygame.image.load(os.path.join(imageFolder, 'quartz.png'))
quartzImg = pygame.transform.scale(quartzImg, (scaleSize, scaleSize))
jadeImg = pygame.image.load(os.path.join(imageFolder, 'jade.png'))
jadeImg = pygame.transform.scale(jadeImg, (scaleSize, scaleSize))
sapphireImg = pygame.image.load(os.path.join(imageFolder, 'sapphire.png'))
sapphireImg = pygame.transform.scale(sapphireImg, (scaleSize, scaleSize))
rubyImg = pygame.image.load(os.path.join(imageFolder, 'ruby.png'))
rubyImg = pygame.transform.scale(rubyImg, (scaleSize, scaleSize))
diamondImg = pygame.image.load(os.path.join(imageFolder, 'diamond.png'))
diamondImg = pygame.transform.scale(diamondImg, (scaleSize, scaleSize))

# buttons displayed at the end of the maze
playAgainImg = pygame.image.load(os.path.join(imageFolder, 'playAgainButton.png'))
playAgainHoverImg = pygame.image.load(os.path.join(imageFolder, 'playAgainButtonHover.png'))
quitMazeImg = pygame.image.load(os.path.join(imageFolder, 'quitMaze.png'))
quitMazeHoverImg = pygame.image.load(os.path.join(imageFolder, 'quitMazeHover.png'))
mazeButtonImgs = [playAgainImg, playAgainHoverImg, quitMazeImg, quitMazeHoverImg]
for i in range(len(mazeButtonImgs)):
    mazeButtonImgs[i] = pygame.transform.scale(mazeButtonImgs[i], (200,125))

# maze end screen
mazeEndBG = pygame.image.load(os.path.join(imageFolder, 'mazeComplete.png'))  
mazeEndBG = pygame.transform.scale(mazeEndBG, (dimensions[0]*resolution, dimensions[1]*resolution)) 

# sprite
spriteImg = pygame.image.load(os.path.join(imageFolder, 'sprite.png'))
spriteImg = pygame.transform.scale(spriteImg, (20, 30))

# image displayed at the start of the game
gameStartImg = pygame.image.load(os.path.join(imageFolder, 'gameStart.png'))
gameStartImg = pygame.transform.scale(gameStartImg, (dimensions[0]*resolution, dimensions[1]*resolution))

# button scaler variables help set the rectangle area where the button is functional, by scaling the image of the button
buttonScalerX = 200
buttonScalerY = 100
# start game buttons displayed when game is first run
startGameImg = pygame.image.load(os.path.join(imageFolder, 'startGame.png'))
startGameImg = pygame.transform.scale(startGameImg, (buttonScalerX, buttonScalerY))
startHoverImg = pygame.image.load(os.path.join(imageFolder, 'startGameHover.png'))
startHoverImg = pygame.transform.scale(startHoverImg, (buttonScalerX, buttonScalerY))

# for the backstory/context screen that explains how to play the game
backstoryImg = pygame.image.load(os.path.join(imageFolder, 'backstory1.png'))
backstoryImg = pygame.transform.scale(backstoryImg, (dimensions[0]*resolution, dimensions[1]*resolution)) 
goToMenuImg = pygame.image.load(os.path.join(imageFolder, 'goToMenu.png'))
goToMenuImg = pygame.transform.scale(goToMenuImg, (buttonScalerX, buttonScalerY))
goToMenuHover = pygame.image.load(os.path.join(imageFolder, 'goToMenuHover.png'))
goToMenuHover = pygame.transform.scale(goToMenuHover, (buttonScalerX, buttonScalerY))

# in game menu background
menuBG = pygame.image.load(os.path.join(imageFolder, 'gameMenu3.png'))
menuBG = pygame.transform.scale(menuBG, (dimensions[0]*resolution, dimensions[1]*resolution))

# shop button on the in-game menu
shopButtonImg = pygame.image.load(os.path.join(imageFolder, 'shopButton.png'))
shopButtonHoverImg = pygame.image.load(os.path.join(imageFolder, 'shopButtonHover.png'))
shopButtonImg = pygame.transform.scale(shopButtonImg, (300, 150))
shopButtonHoverImg = pygame.transform.scale(shopButtonHoverImg, (300, 150))

# maze button on the in-game menu
mazeButtonImg = pygame.image.load(os.path.join(imageFolder, 'mazeButton.png'))
mazeButtonHoverImg = pygame.image.load(os.path.join(imageFolder, 'mazeButtonHover.png'))
mazeButtonImg = pygame.transform.scale(mazeButtonImg, (300, 150))
mazeButtonHoverImg = pygame.transform.scale(mazeButtonHoverImg, (300, 150))

# progress tracker button on the in-game menu
progressTrackerButtonImg = pygame.image.load(os.path.join(imageFolder, 'progressTrackerButton.png'))
progressTrackerButtonHoverImg = pygame.image.load(os.path.join(imageFolder, 'progressTrackerButtonHover.png'))
progressTrackerButtonImg = pygame.transform.scale(progressTrackerButtonImg, (300, 150))
progressTrackerButtonHoverImg = pygame.transform.scale(progressTrackerButtonHoverImg, (300, 150))

# battle button on the in-game menu
battleButtonImg = pygame.image.load(os.path.join(imageFolder, 'battleButton.png'))
battleButtonHoverImg = pygame.image.load(os.path.join(imageFolder, 'battleButtonHover.png'))
battleButtonImg = pygame.transform.scale(battleButtonImg, (300, 150))
battleButtonHoverImg = pygame.transform.scale(battleButtonHoverImg, (300, 150))

# images of weapons in the shop (not of the weapons in battle)
swordI_img = pygame.image.load(os.path.join(imageFolder, 'swordI.png'))
swordI_altImg = pygame.image.load(os.path.join(imageFolder, 'swordI_alt.png'))
swordII_img = pygame.image.load(os.path.join(imageFolder, 'swordII.png'))
swordII_altImg = pygame.image.load(os.path.join(imageFolder, 'swordII_alt.png'))
swordIII_img = pygame.image.load(os.path.join(imageFolder, 'swordIII.png'))
swordIII_altImg = pygame.image.load(os.path.join(imageFolder, 'swordIII_alt.png'))
pistol_img = pygame.image.load(os.path.join(imageFolder, 'pistol.png'))
pistol_altImg = pygame.image.load(os.path.join(imageFolder, 'pistol_alt.png'))
bow_img = pygame.image.load(os.path.join(imageFolder, 'bow.png'))
bow_altImg = pygame.image.load(os.path.join(imageFolder, 'bow_alt.png'))
flameBow_img = pygame.image.load(os.path.join(imageFolder, 'flameBow.png'))
flameBow_altImg = pygame.image.load(os.path.join(imageFolder, 'flameBow_alt.png'))

# the scaling for shop images
scalingFactors = (700, 140)

# list of images is assigned and iterated through in order to scale all images to the same amount of pixels
shopImgList = [swordI_img, swordI_altImg, swordII_img, swordII_altImg, swordIII_img, swordIII_altImg, pistol_img, pistol_altImg, bow_img, bow_altImg, flameBow_img, flameBow_altImg]
for i in range(0, len(shopImgList)):
    shopImgList[i] = pygame.transform.scale(shopImgList[i], scalingFactors)

# setting width and height to form the rectangle area of the button 
purchaseButtonWidth = 100 
purchaseButtonHeight = 30
# purchase button images for the shop
purchaseButton_img = pygame.image.load(os.path.join(imageFolder, 'purchaseButton.png'))
purchaseButton_hoverImg = pygame.image.load(os.path.join(imageFolder, 'purchaseButton_hover.png'))
purchaseButton_img = pygame.transform.scale(purchaseButton_img, (purchaseButtonWidth, purchaseButtonHeight))
purchaseButton_hoverImg = pygame.transform.scale(purchaseButton_hoverImg, (purchaseButtonWidth, purchaseButtonHeight))

# back button for shop/progress tracker/maze
backButtonImg = pygame.image.load(os.path.join(imageFolder, 'backButton.png'))
backButtonImg = pygame.transform.scale(backButtonImg, (20,20)) 
backButtonHoverImg = pygame.image.load(os.path.join(imageFolder, 'backButtonHover.png'))
backButtonHoverImg = pygame.transform.scale(backButtonHoverImg, (20,20))

# labels for progress tracker
levelImg = pygame.image.load(os.path.join(imageFolder, 'levelLabel.png'))
levelImg = pygame.transform.scale(levelImg, (150, 50))
damageImg = pygame.image.load(os.path.join(imageFolder, 'damageLabel.png'))
damageImg = pygame.transform.scale(damageImg, (150,50))

# battle backgrounds for each level
snowBG = pygame.image.load(os.path.join(imageFolder, 'snowstorm.png'))
snowBG = pygame.transform.scale(snowBG, (dimensions[0]*resolution, dimensions[1]*resolution))
forestBG = pygame.image.load(os.path.join(imageFolder, 'forest.png'))
forestBG = pygame.transform.scale(forestBG, (dimensions[0]*resolution, dimensions[1]*resolution))
abandonedRoomBG = pygame.image.load(os.path.join(imageFolder, 'abandonedRoom.png'))
abandonedRoomBG = pygame.transform.scale(abandonedRoomBG, (dimensions[0]*resolution, dimensions[1]*resolution))
desertBG = pygame.image.load(os.path.join(imageFolder, 'desert.png'))
desertBG = pygame.transform.scale(desertBG, (dimensions[0]*resolution, dimensions[1]*resolution))
caveBG = pygame.image.load(os.path.join(imageFolder, 'cave.png'))
caveBG = pygame.transform.scale(caveBG, (dimensions[0]*resolution, dimensions[1]*resolution))


# obstacle images for each level
obstacleScale = 60
snowObstacleImg = pygame.image.load(os.path.join(imageFolder, 'snowObstacle.png'))
snowObstacleImg = pygame.transform.scale(snowObstacleImg, (obstacleScale, obstacleScale))
flowerObstacleImg = pygame.image.load(os.path.join(imageFolder, 'flowerObstacle.png'))
flowerObstacleImg = pygame.transform.scale(flowerObstacleImg, (obstacleScale, obstacleScale))
caveObstacleImg = pygame.image.load(os.path.join(imageFolder, 'caveObstacle.png'))
caveObstacleImg = pygame.transform.scale(caveObstacleImg, (obstacleScale, obstacleScale))
crateObstacleImg = pygame.image.load(os.path.join(imageFolder, 'crateObstacle.png'))
crateObstacleImg = pygame.transform.scale(crateObstacleImg, (obstacleScale*0.75, obstacleScale*0.75))
rockObstacleImg = pygame.image.load(os.path.join(imageFolder, 'rockObstacle.png'))
rockObstacleImg = pygame.transform.scale(rockObstacleImg, (obstacleScale, obstacleScale))

# enemy images
enemyImgScale = 40
trollImg = pygame.image.load(os.path.join(imageFolder, 'troll.png'))
trollImg = pygame.transform.scale(trollImg, (enemyImgScale, enemyImgScale))
phantomImg = pygame.image.load(os.path.join(imageFolder, 'phantom.png'))
phantomImg = pygame.transform.scale(phantomImg, (enemyImgScale, enemyImgScale))
shadowMonsterImg = pygame.image.load(os.path.join(imageFolder, 'shadowMonster.png'))
shadowMonsterImg = pygame.transform.scale(shadowMonsterImg, (enemyImgScale*0.7, enemyImgScale))
dragonImg = pygame.image.load(os.path.join(imageFolder, 'dragon.png'))
dragonImg = pygame.transform.scale(dragonImg, (enemyImgScale*1.5, enemyImgScale*1.5))

# enemy projectiles
projectileScale = 30
phantomProjectileImg = pygame.image.load(os.path.join(imageFolder, 'phantomProjectile.png'))
phantomProjectileImg = pygame.transform.scale(phantomProjectileImg, (projectileScale, projectileScale)) 
dragonProjectileImg = pygame.image.load(os.path.join(imageFolder, 'dragonProjectile.png'))
dragonProjectileImg = pygame.transform.scale(dragonProjectileImg, (projectileScale*0.5, projectileScale*0.5))

# player projectiles
bulletImg = pygame.image.load(os.path.join(imageFolder, 'bullet.png'))
bulletImg = pygame.transform.scale(bulletImg, (projectileScale, projectileScale))
arrowImg = pygame.image.load(os.path.join(imageFolder, 'arrow.png'))
arrowImg = pygame.transform.scale(arrowImg, (projectileScale*2, projectileScale*2))
flameArrowImg = pygame.image.load(os.path.join(imageFolder, 'flameArrow.png'))
flameArrowImg = pygame.transform.scale(flameArrowImg, (projectileScale*2, projectileScale*2))

# battle outcome backgrounds and buttons
battleWonImg = pygame.image.load(os.path.join(imageFolder, 'wonBattle.png'))
battleLostImg = pygame.image.load(os.path.join(imageFolder, 'lostBattle.png'))
battleWonImg = pygame.transform.scale(battleWonImg, (dimensions[0]*resolution, dimensions[1]*resolution))
battleLostImg = pygame.transform.scale(battleLostImg, (dimensions[0]*resolution, dimensions[1]*resolution))
playBattleImg = pygame.image.load(os.path.join(imageFolder, 'playBattleButton.png'))
playBattleHoverImg = pygame.image.load(os.path.join(imageFolder, 'playBattleButtonHover.png'))
gameMenuButtonImg = pygame.image.load(os.path.join(imageFolder, 'gameMenuButton.png'))
gameMenuButtonHoverImg = pygame.image.load(os.path.join(imageFolder, 'gameMenuButtonHover.png'))
# scaling each button image 
buttonImgs = [playBattleImg, playBattleHoverImg, gameMenuButtonImg, gameMenuButtonHoverImg]
for i in range(len(buttonImgs)):
    buttonImgs[i] = pygame.transform.scale(buttonImgs[i], (300,100))

# game final outcome images - game won or game lost
gameWonImg = pygame.image.load(os.path.join(imageFolder, 'gameWon.png'))
gameLostImg = pygame.image.load(os.path.join(imageFolder, 'gameLost.png'))
gameWonImg = pygame.transform.scale(gameWonImg, (dimensions[0]*resolution, dimensions[1]*resolution))
gameLostImg = pygame.transform.scale(gameLostImg, (dimensions[0]*resolution, dimensions[1]*resolution))

# images of numbers/dollar sign to display money count on screen
img0 = pygame.image.load(os.path.join(imageFolder, 'zero.png'))
img1 = pygame.image.load(os.path.join(imageFolder, 'one.png'))
img2 = pygame.image.load(os.path.join(imageFolder, 'two.png'))
img3 = pygame.image.load(os.path.join(imageFolder, 'three.png'))
img4 = pygame.image.load(os.path.join(imageFolder, 'four.png'))
img5 = pygame.image.load(os.path.join(imageFolder, 'five.png'))
img6 = pygame.image.load(os.path.join(imageFolder, 'six.png'))
img7 = pygame.image.load(os.path.join(imageFolder, 'seven.png'))
img8 = pygame.image.load(os.path.join(imageFolder, 'eight.png'))
img9 = pygame.image.load(os.path.join(imageFolder, 'nine.png'))
currencyImg = pygame.image.load(os.path.join(imageFolder, 'currency.png'))
numListImgs = [img0, img1, img2, img3, img4, img5, img6, img7, img8, img9, currencyImg]

# scaling of images needed for displaying money count
for i in range(len(numListImgs)): 
    numListImgs[i] = pygame.transform.scale(numListImgs[i], (20,20))

# image of a blank inventory slot
invSlotImg = pygame.image.load(os.path.join(imageFolder, 'emptyInventorySlot.png'))
invSlotSize = 60
invSlotImg = pygame.transform.scale(invSlotImg, (invSlotSize, invSlotSize))


# weapon image icons for inventory
swordI_icon = pygame.image.load(os.path.join(imageFolder, 'SRweapon1.png'))
swordI_icon = pygame.transform.scale(swordI_icon, (20, 50))
swordII_icon = pygame.image.load(os.path.join(imageFolder, 'SRweapon2.png'))
swordII_icon = pygame.transform.scale(swordII_icon, (20, 50))
swordIII_icon = pygame.image.load(os.path.join(imageFolder, 'SRweapon3.png'))
swordIII_icon = pygame.transform.scale(swordIII_icon, (20, 50))
pistol_icon = pygame.image.load(os.path.join(imageFolder, 'pistol_icon.png'))
pistol_icon = pygame.transform.scale(pistol_icon, (40, 50))
bow_icon = pygame.image.load(os.path.join(imageFolder, 'bowIcon.png'))
bow_icon = pygame.transform.scale(bow_icon, (20, 50))
flameBow_icon = pygame.image.load(os.path.join(imageFolder, 'flameBowIcon.png'))
flameBow_icon = pygame.transform.scale(flameBow_icon, (20, 50))

# actual weapon images - needed for ShortRangeWeapon class weapons to be displayed in animations during battle
# these images are rotated so they will be displayed at an angle when used in animations
weaponScaler = 50
swordI_actualImg = pygame.transform.scale(swordI_icon, (weaponScaler, weaponScaler))
swordI_actualImg = pygame.transform.rotate(swordI_actualImg, -90)
swordII_actualImg = pygame.transform.scale(swordII_icon, (weaponScaler, weaponScaler))
swordII_actualImg = pygame.transform.rotate(swordII_actualImg, -90)
swordIII_actualImg = pygame.transform.scale(swordIII_icon, (weaponScaler, weaponScaler))
swordIII_actualImg = pygame.transform.rotate(swordIII_actualImg, -90)
