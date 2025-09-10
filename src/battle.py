# file for all battle-related code 

import pygame
pygame.init()
from random import randint
import time 

# getting the time is useful for handling enemy attack cooldowns and the reset time for enemy projectiles
clock = pygame.time.Clock() 

# importing other files here
from gameData import * 
from soundFile import *
from intro import *
from imageData import *

# sets relevant data about the level like background and obstacle theme
def setLevel(level): 
    if level == 1:
        backgroundImg = snowBG
        obstacleImg = snowObstacleImg
    if level == 2:
        backgroundImg = forestBG
        obstacleImg = flowerObstacleImg
    if level == 3:
        backgroundImg = abandonedRoomBG
        obstacleImg = crateObstacleImg
    if level == 4:
        backgroundImg = desertBG
        obstacleImg = rockObstacleImg
    if level == 5:
        backgroundImg = caveBG
        obstacleImg = caveObstacleImg
    
    obstacleNum = randint(10, 20) # random number of obstacles on each level for variety
    return [backgroundImg, obstacleImg, obstacleNum] # list is returned so relevant data about the level can be easily accessed

# generates obstacles for the particular battle
def setObstacles(levelData): # levelData will be obtained from calling the setLevel function
    obstacleList = []
    obstacleImg = levelData[1]
    obstacleNum = levelData[2]
    for i in range(obstacleNum): 
        validLoc = False 
        while not validLoc: # generates a position for each obstacle until a valid one is found 
            x = randint(minX, (maxX - 50))
            y = randint((minY + 200), (maxY - 250))
            newObstacle = Obstacle(x, y, obstacleImg)
            validLoc = True
            for obstacle in obstacleList: # runs through all obstacles to ensure new obstacle doesn't generate on top of existing ones
                offset = (newObstacle.x - obstacle.x, newObstacle.y - obstacle.y)
                collision = obstacle.mask.overlap(newObstacle.mask, offset) 
                if collision: 
                    validLoc = False 
            if x > 225 and x < 610 and y > (maxY - 145) and y < (maxY - 50): # obstacles cannot be generated in inventory area
                validLoc = False
            if x > (maxX - 100) and y > (maxY - 265): # obstacles cannot be generated in health bar area
                validLoc = False 
        # once a position is generated that satisfies all conditions, it is added to a list of obstacles so it can be kept track of
        obstacleList.append(newObstacle)
    return obstacleList 

# iterates through list to render obstacles
def showObstacles(gameObstacles): 
    for obstacle in gameObstacles:
        obstacle.renderObstacle()

# attack of enemy is based on modifying baseAttack value according to the particular level, as levels increase in difficulty
baseAttack = 1

# generates troll enemy type on all levels
def setTrolls(baseAttack, level, obstacleList): 
    attack = baseAttack + (level-1)*2
    trollList = [] 
    for i in range(5):
        validLoc = False 
        while not validLoc: # generates a starting position for enemies until a valid one is found
            x = randint(minX, (maxX - 50))
            y = randint((minY + 200), (maxY - 250)) 
            newTroll = ShortRangeEnemy(trollImg, attack, x, y, 3)
            validLoc = True
            for troll in trollList: # enemies must not generate on top of other enemies
                offset = (newTroll.x - troll.x, newTroll.y - troll.y)
                collision = troll.mask.overlap(newTroll.mask, offset)
                if collision:
                    validLoc = False 
            for obstacle in obstacleList: # enemies must not generate on top of obstacles
                offset = (newTroll.x - obstacle.x, newTroll.y - obstacle.y)
                collision = obstacle.mask.overlap(newTroll.mask, offset)
                if collision:
                    validLoc = False
            if x > 225 and x < 610 and y > (maxY - 145) and y < (maxY - 50): # enemies cannot be generated in inventory area
                validLoc = False
            elif x > (maxX - 100) and y > (maxY - 265): # enemies cannot be generated in health bar area
                validLoc = False 
        # once a position is generated that satisfies all conditions, it is added to a list of enemies so it can be kept track of
        trollList.append(newTroll)
    return trollList

# generates phantom enemy type on all levels
def setPhantoms(baseAttack, level, obstacleList, trollList):
    attack = baseAttack + (level-1)*2
    phantomList = []
    for i in range(5):
        validLoc = False 
        while not validLoc: # generates a starting position for enemies until a valid one is found
            x = randint(minX, (maxX - 50))
            y = randint((minY + 200), (maxY - 250))
            newPhantom = LongRangeEnemy(phantomImg, attack, x, y)
            validLoc = True
            for obstacle in obstacleList: # enemies need to not generate on top of obstacles
                offset = (newPhantom.x - obstacle.x, newPhantom.y - obstacle.y)
                collision = obstacle.mask.overlap(newPhantom.mask, offset)
                if collision:
                    validLoc = False
            # enemies must not generate on top of other enemies 
            for troll in trollList: 
                offset = (newPhantom.x - troll.x, newPhantom.y - troll.y)
                collision = troll.mask.overlap(newPhantom.mask, offset)
                if collision:
                    validLoc = False
            for phantom in phantomList:
                offset = (newPhantom.x - phantom.x, newPhantom.y - phantom.y)
                collision = phantom.mask.overlap(newPhantom.mask, offset)
                if collision:
                    validLoc = False
            if x > 225 and x < 610 and y > (maxY - 145) and y < (maxY - 50): # enemies cannot be generated in inventory area
                validLoc = False
            elif x > (maxX - 100) and y > (maxY - 265): # enemies cannot be generated in health bar area
                validLoc = False 
        # once a position is generated that satisfies all conditions, it is added to a list of enemies so it can be kept track of
        phantomList.append(newPhantom)
    return phantomList

# only run if level 5
def setShadowMonsters(obstacleList, trollList, phantomList):
    attack = 5
    shadowMonsterList = []
    for i in range(5):
        validLoc = False 
        while not validLoc: # generates a starting position for enemies until a valid one is found
            x = randint(minX, (maxX - 50))
            y = randint((minY + 200), (maxY - 250))
            newShadowMonster = ShortRangeEnemy(shadowMonsterImg, attack, x, y, 3)
            validLoc = True
            for obstacle in obstacleList: # enemies need to not generate on top of obstacles
                offset = (newShadowMonster.x - obstacle.x, newShadowMonster.y - obstacle.y)
                collision = obstacle.mask.overlap(newShadowMonster.mask, offset)
                if collision:
                    validLoc = False
            # enemies must not generate on top of other enemies 
            for troll in trollList: 
                offset = (newShadowMonster.x - troll.x, newShadowMonster.y - troll.y)
                collision = troll.mask.overlap(newShadowMonster.mask, offset)
                if collision:
                    validLoc = False
            for phantom in phantomList:
                offset = (newShadowMonster.x - phantom.x, newShadowMonster.y - phantom.y)
                collision = phantom.mask.overlap(newShadowMonster.mask, offset)
                if collision:
                    validLoc = False
            for shadowMonster in shadowMonsterList:
                offset = (newShadowMonster.x - shadowMonster.x, newShadowMonster.y - shadowMonster.y)
                collision = shadowMonster.mask.overlap(newShadowMonster.mask, offset)
                if collision:
                    validLoc = False
            if x > 225 and x < 610 and y > (maxY - 145) and y < (maxY - 50): # enemies cannot be generated in inventory area
                validLoc = False
            elif x > (maxX - 100) and y > (maxY - 265): # enemies cannot be generated in health bar area
                validLoc = False 
        # once a position is generated that satisfies all conditions, it is added to a list of enemies so it can be kept track of
        shadowMonsterList.append(newShadowMonster)
    return shadowMonsterList

# only run if level 5 
def setDragons(obstacleList, trollList, phantomList, shadowMonsterList):
    attack = 5
    dragonList = []
    for i in range(5):
        validLoc = False 
        while not validLoc: # generates a starting position for enemies until a valid one is found
            x = randint(minX, (maxX - 50))
            y = randint((minY + 200), (maxY - 250))
            newDragon = LongRangeEnemy(dragonImg, attack, x, y)
            validLoc = True
            for obstacle in obstacleList: # enemies need to not generate on top of obstacles
                offset = (newDragon.x - obstacle.x, newDragon.y - obstacle.y)
                collision = obstacle.mask.overlap(newDragon.mask, offset)
                if collision:
                    validLoc = False
            # enemies must not generate on top of other enemies 
            for troll in trollList: 
                offset = (newDragon.x - troll.x, newDragon.y - troll.y)
                collision = troll.mask.overlap(newDragon.mask, offset)
                if collision:
                    validLoc = False
            for phantom in phantomList:
                offset = (newDragon.x - phantom.x, newDragon.y - phantom.y)
                collision = phantom.mask.overlap(newDragon.mask, offset)
                if collision:
                    validLoc = False
            for shadowMonster in shadowMonsterList:
                offset = (newDragon.x - shadowMonster.x, newDragon.y - shadowMonster.y)
                collision = shadowMonster.mask.overlap(newDragon.mask, offset)
                if collision:
                    validLoc = False
            for dragon in dragonList:
                offset = (newDragon.x - dragon.x, newDragon.y - dragon.y)
                collision = newDragon.mask.overlap(newDragon.mask, offset)
                if collision:
                    validLoc = False
            if x > 225 and x < 610 and y > (maxY - 145) and y < (maxY - 50): # enemies cannot be generated in inventory area
                validLoc = False
            elif x > (maxX - 100) and y > (maxY - 265): # enemies cannot be generated in health bar area
                validLoc = False 
        # once a position is generated that satisfies all conditions, it is added to a list of enemies so it can be kept track of
        dragonList.append(newDragon)
    return dragonList

# wraps instantiation of enemies into one function
def setEnemies(baseAttack, level, obstacleList): 
    trollList = setTrolls(baseAttack, level, obstacleList)
    phantomList = setPhantoms(baseAttack, level, obstacleList, trollList)
    enemyList = [trollList, phantomList]
    if level > 4: # accounts for the other set of enemies that need to be instantiated
        shadowMonsterList = setShadowMonsters(obstacleList, trollList, phantomList)
        dragonList = setDragons(obstacleList, trollList, phantomList, shadowMonsterList)
        enemyList.append(shadowMonsterList)
        enemyList.append(dragonList)
    return enemyList 

# resets / gets sprite ready for (a new) battle
def initialiseSprite(obstacleList):
    validPos = False
    count = 0
    x = 100
    y = 300
    # allows the position to be regenerated until the user is set in a valid position (i.e. not on top of an obstacle as it will be unable to move)
    # the count variable ensures an infinite loop error will not occur
    while not(validPos) and count < 300: 
        obsCollision = sprite.obstacleCheck(x, y, obstacleList)
        if not obsCollision:
            validPos = True 
            sprite.setStartPos(x, y)
        else:
            x += 2
    sprite.setSpeed(5) # speed will be different between maze and battle so must be set before battle
    sprite.resize(30, 45) # size of character is also different between maze and battle
    sprite.resetHealth()

# draws all enemies onto the screen, and their corresponding projectiles 
# removes from existence any enemies whose health have run out, and their corresponding projectiles
def renderEnemies(enemyList, activeProjectiles, inactiveProjectiles): 
    for enemy in enemyList[0]:
        if enemy.health <= 0: 
            enemyList[0].remove(enemy)
        else: 
            enemy.renderEnemy()
    for enemy in enemyList[1]:
        if enemy.health <= 0: # if it's dead I need to remove its projectile also by finding the projectile with a matching starting position
            # the corresponding projectile may be inactive (about to be fired) or active, so both lists need to be checked
            for projectile in activeProjectiles:
                if projectile.startingX == enemy.x and projectile.startingY == enemy.y: 
                    activeProjectiles.remove(projectile)
            for projectile in inactiveProjectiles:
                if projectile.startingX == enemy.x and projectile.startingY == enemy.y:
                    inactiveProjectiles.remove(projectile)
            enemyList[1].remove(enemy) 
        else:
            enemy.renderEnemy() # otherwise if not dead just render as usual
    if len(enemyList) > 2: # i.e. 4 types of enemy on the level, not 2, as is the case on level 5
        for enemy in enemyList[2]:
            if enemy.health <= 0:
                enemyList[2].remove(enemy)
            else:
                enemy.renderEnemy()
        for enemy in enemyList[3]:
            if enemy.health <= 0: # if it's dead I need to remove its projectile also by finding the projectile with a matching starting position
                # the corresponding projectile may be inactive (about to be fired) or active, so both lists need to be checked
                for projectile in activeProjectiles: 
                    if projectile.startingX == enemy.x and projectile.startingY == enemy.y:
                        activeProjectiles.remove(projectile)
                for projectile in inactiveProjectiles:
                    if projectile.startingX == enemy.x and projectile.startingY == enemy.y:
                        inactiveProjectiles.remove(projectile)
                enemyList[3].remove(enemy)
            else:
                enemy.renderEnemy()

# allows for user movement in battle, taking into account the list of obstacles and enemies
def moveUser(obstacleList, enemyList): 
    keys = pygame.key.get_pressed()
    sprite.battleMovement(keys, obstacleList, enemyList)

# useful details for drawing the health bar in the bottom right corner of the screen
startingX = maxX - 60
startingY = maxY - 200
height = 200
# function for drawing health bar using a white background rectangle and green smaller rectangles
def setHealthBar(x, y, height): # pass in startingX and startingY so they can be modified without issues, along with height
    healthAmt = sprite.getHealth()
    barRect = pygame.Rect(x, y, 50, height) # the rectangular bar that all health points will be drawn onto 
    pygame.draw.rect(display, 'gray89', barRect) 
    barHeight = height / 115 # height of each individual health point, max 115
    currentY = y + height # as health bar is drawn bottom-up, not top-down
    for healthPoint in range(healthAmt): # draws each health point onto the health bar 
        currentY -= barHeight 
        rectHP = pygame.Rect(x+3, currentY, 44, barHeight)
        # health bar might be drawn as red if health is low, green otherwise
        # two different colour shades are used for the health bar so each individual health point is visible / it is easier to see when health points decrease
        if healthPoint % 2 == 0 and healthAmt > 30: 
            pygame.draw.rect(display, 'green', rectHP)
        elif healthPoint % 2 == 0: 
            pygame.draw.rect(display, 'red', rectHP)
        elif healthAmt > 30: 
            pygame.draw.rect(display, '#07e136', rectHP)
        else: 
            pygame.draw.rect(display, 'orange', rectHP)

# health bar is labelled to make it clear to the player what it is and exactly how much health they have left
def labelHealthBar(x, y):
    font = pygame.font.Font('freesansbold.ttf', 15) # sets font
    text = 'health: ' + str(sprite.getHealth()) # concatenates label with actual health value 
    healthText = font.render(text, True, ('red'))
    healthTextRect = healthText.get_rect()
    healthTextRect.center = (x, y)
    display.blit(healthText, healthTextRect) 

# general function for getting slot that was clicked / highlighting it
def getSlot(event, inventory): # event must be checked for mouse button down before being passed in
    mouse_pos = event.pos # gets mouse position
    for index, slot in enumerate(inventory.mainInventory):
        if slot[2].collidepoint(mouse_pos): # slot[2] is the rect object of the slot, used to check for a collision
            inventory.setCurrentWeapon(index) # sets current weapon based on slot contents - could be None too. If it is a weapon, it will be used when the player clicks on the screen
            return slot # terminates function once found

# clicks during battle may be for using a weapon or for interacting with the inventory; this function checks if is a click for using a weapon
def checkWeaponClick(event, inventory):
    mouse_pos = event.pos
    for slot in inventory.mainInventory: # iterates through each slot to check for click on any of the 6 slots
        if slot[2].collidepoint(mouse_pos): # slot[2] is the rect object of the slot, which is needed to check for a collision 
            return False 
    return True 

# function wrapping all other functions succinctly into one, sets up the battle (not including enemies)
def setBattle(levelData, obstacleList, startingX, startingY, height, enemyList): 
    setBG(levelData[0])
    showObstacles(obstacleList)
    moveUser(obstacleList, enemyList)
    sprite.renderSprite()
    setHealthBar(startingX, startingY, height)
    labelHealthBar(startingX+20, startingY-12)
    userInventory.render_inventory()


# initialises projectiles for long-range enemies - these objects are aimed in the player's direction, and an enemy will keep firing them until they die
def setProjectiles(enemyList):
    inactiveProjectiles = [] # all projectiles begin as inactive, so must all be generated and added to this list
    for enemy in enemyList[1]: # for each enemy, a projectile must be made, using the enemy x and y position as startingX and startingY so it originates from that enemy
        projectile = EnemyProjectile(enemy.x, enemy.y, phantomProjectileImg, 7, enemy.damage)
        projectile.saveStartingPos() # starting position of projectile must be retained so it always fires from the same position
        inactiveProjectiles.append(projectile) 
    if len(enemyList) > 2: # indicates the level is 5, so there are 2 types of long-range enemies to account for
        for enemy in enemyList[3]:
            projectile = EnemyProjectile(enemy.x, enemy.y, dragonProjectileImg, 7, enemy.damage)
            projectile.saveStartingPos()
            inactiveProjectiles.append(projectile)
    return inactiveProjectiles

# function for updating the timer on enemy projectiles; when their timer is up, they become active and fire at the player
def updateTimer(inactiveProjectiles, time, activeProjectiles):
    for projectile in inactiveProjectiles:
        projectile.time -= time
        if projectile.time <= 0:
            activeProjectiles.append(projectile) # now becomes an active projectile
            projectile.setTrajectory(sprite.x, sprite.y) # its path is set, it fires in the player's direction
            inactiveProjectiles.remove(projectile) # no longer an inactive projectile

# handles active projectiles by rendering them, or resetting them if they collided with an obstacle/player/screen boundary (indicated by projectile's attribute "finished")
def handleActiveProjectiles(activeProjectiles, inactiveProjectiles, obstacleList):
    for projectile in activeProjectiles:
        if projectile.finished == True: 
            projectile.resetProjectile() # resets projectile including "finished" attribute, timer and location
            inactiveProjectiles.append(projectile) # sets it as an inactive projectile again which will run in the future
            activeProjectiles.remove(projectile) # removes from active projectiles
        else: # projectile is active, continues to render on the screen 
            projectile.renderProjectile()
            projectile.moveProjectile(sprite, obstacleList)
    
# handles short range enemy movement
# short range enemies have an attack cooldown so they can't continuously attack the player when in contact, otherwise it would be too difficult to play
# short range enemies have a diversion cooldown, this is where,  if they collide with an obstacle or other enemy, they are temporarily diverted in another direction until the cooldown is over
def handleShortRangeEnemies(enemyList, obstacleList, time):
    for enemy in enemyList[0]:
        enemy.enemyMovement(obstacleList, sprite, enemyList)
        enemy.handleAttackCooldown(time) 
        enemy.handleDiversionCooldown() # does not take time as a parameter as it uses number of frames instead
    if len(enemyList) > 2: # indicates level 5, so 2 types of short-range enemy are present
        for enemy in enemyList[2]:
            enemy.enemyMovement(obstacleList, sprite, enemyList)
            enemy.handleAttackCooldown(time)
            enemy.handleDiversionCooldown() # does not take time as a parameter as it uses number of frames instead

# wraps functions related to enemy handling into one subroutine for convenience in main.py
def allEnemyHandling(enemyList, time, activeProjectiles, inactiveProjectiles, obstacleList): 
    handleShortRangeEnemies(enemyList, obstacleList, time)
    renderEnemies(enemyList, activeProjectiles, inactiveProjectiles)
    updateTimer(inactiveProjectiles, time, activeProjectiles)
    handleActiveProjectiles(activeProjectiles, inactiveProjectiles, obstacleList)

# checks which weapon is currently highlighted (i.e. in use) in inventory and carries out the appropriate preparation for the weapon to be used
def fireWeapon(event, inventory, playerProjectileList): 
    mouse_x, mouse_y = event.pos
    weapon = inventory.weaponInUse
    longRangeWeapon = False # starts false by default until a long range weapon is checked and this is set to true
    # if it is a short-range weapon, it prepares for the weapon to be swung in the direction that the player clicked in
    if (weapon == swordI or weapon == swordII or weapon == swordIII) and weapon.cooldown == False:
        weapon.getDirection(mouse_x, mouse_y, sprite.x, sprite.y)
        weapon.setUpWeapon()
    # if the weapon in use is long-range, a new projectile object is generated and added to the list PlayerProjectile to be kept track of
    elif weapon == pistol:
        projectile = PlayerProjectile(sprite.x, sprite.y, bulletImg, 7, pistol.damage)
        longRangeWeapon = True
    elif weapon == bow:
        projectile = PlayerProjectile(sprite.x, sprite.y, arrowImg, 7, bow.damage)
        longRangeWeapon = True
    elif weapon == flameBow:
        projectile = PlayerProjectile(sprite.x, sprite.y, flameArrowImg, 7, flameBow.damage)
        longRangeWeapon = True
    if longRangeWeapon: 
        projectile.setTrajectory(mouse_x, mouse_y) # projectile is fired in the direction the player clicked in
        projectile.rotateProjectile() # projectile must be rotated appropriately based on the direction it is meant to fire in
        playerProjectileList.append(projectile)
    pygame.mixer.Sound.play(weaponSound)
    return playerProjectileList

# deals with player projectiles, moving and rendering them, or removing them from existence if they have collided with something (meaning they have run their course)
def handleWeaponProjectiles(projectileList, obstacleList, enemyList):
    for projectile in projectileList: 
        if projectile.finished == False:
            projectile.moveProjectile(obstacleList, enemyList)
            projectile.renderProjectile()
        else:
            projectileList.remove(projectile) # removes projectile from existence once it has run its course (attribute finished = True)

# instantiation of buttons needed once the game terminates
playBattle = Button(maxX*0.2, maxY*0.7, 300, 100, buttonImgs[0], buttonImgs[1])
quitBattle = Button(maxX*0.5, maxY*0.7, 300, 100, buttonImgs[2], buttonImgs[3])

# runs every frame to check if the game has terminated yet
def checkEndGame(enemyList):
    end = True # starts as true, and remains until shown to be false
    if sprite.getHealth() <= 0: # game must be over if sprite health is 0 so can automatically return end as True
        return end
    for list in enemyList: # else must check each enemy list to see if all enemies have health 0 so no longer exist
        if list != []:
            end = False
    return end 

# checks if battle has been won
def battleWon(): 
    if sprite.getHealth() <= 0:
        return False
    else:
        return True 

