# this file contains class definitions of the main entities in the game

import pygame
pygame.init()

from random import randint
import random
import math
import time

from soundFile import *
from imageData import *


# representing maximum and minimum screen dimensions
maxX = dimensions[0] * resolution
minX = 0
maxY = dimensions[1] * resolution
minY = 0

class Character:
    def __init__(self, x, y, speed, spriteImg):
        self.x = x
        self.y = y
        self.speed = speed
        self.spriteImg = spriteImg
        self.health = 115 # default value, as with enemies
        self.mask = pygame.mask.from_surface(self.spriteImg) # for collision checking with other entities

    def getHealth(self): 
        return self.health 

    def resetHealth(self): 
        self.health = 115 
    
    def setStartPos(self, x, y): # sets starting position of sprite as it may vary between battle and maze
        self.x = x
        self.y = y

    def resize(self, scaleX, scaleY): # resizes sprite as it may vary between battle and maze
        self.spriteImg = pygame.transform.scale(spriteImg, (scaleX, scaleY))

    def setSpeed(self, value): # speed varies between battle and maze
        self.speed = value 

    def renderSprite(self):
        display.blit(self.spriteImg, (self.x, self.y))

    def removeHP(self, damage): # if in collision with an enemy or its projectiles, sprite health will be removed accordingly
        self.health -= damage 

    # checks if a particular move within the maze is valid, or if it would cause the player to go through the maze walls
    def movementCheck(self, grid): 
        for row in grid:
            for tile in row:
                for wallMask, wallPosition in tile.wallMasks:
                    # offset between wall position and sprite 
                    offset = (wallPosition[0] - self.x), (wallPosition[1] - self.y)
                    if self.mask.overlap(wallMask, (offset)):
                        return True 
        return False 

    # carries out actual movement of sprite in maze, by calling movementCheck method to ensure validity of the movement
    def mazeMovement(self, keys, grid): 
        tempX = self.x
        tempY = self.y
        if keys[pygame.K_a]:  
            tempX -= self.speed
        if keys[pygame.K_d]: 
            tempX += self.speed
        if keys[pygame.K_w]:  
            tempY -= self.speed
        if keys[pygame.K_s]:  
            tempY += self.speed 
        # saving original position of sprite
        oldX = self.x
        oldY = self.y
        # assigning new values to x and y of sprite so they can be checked
        self.x = tempX
        self.y = tempY 
        if self.movementCheck(grid): # if collision is detected, x and y position go back to their original values
            self.x = oldX
            self.y = oldY 
    
    # used for checking collision with obstacles, health bar or inventory during battle, as a player movement in battle is invalid if the player would collide with any of these
    def obstacleCheck(self, x, y, obsList): 
        # iterates through every obstacle to ensure no collision with any of them
        for obstacle in obsList:
            offset = (obstacle.x - x, obstacle.y - y)
            if sprite.mask.overlap(obstacle.mask, offset): 
                return True
        # for inventory
        if x > 225 and x < 610 and y > (maxY - 145) and y < (maxY - 50):
            return True
        # for health bar
        if x > (maxX - 100) and y > (maxY - 265):
            return True 
        return False 

    # checks if player movement in battle would be invalid by checking if the player would collide with any enemies
    def enemyCheck(self, x, y, enemyList): 
        for list in enemyList:
            for enemy in list:
                offset = (x - enemy.x, y - enemy.y)
                if enemy.mask.overlap(self.mask, offset):
                    return True
        return False 

    # checks if player movement in battle would be invalid due to exceeding screen boundaries
    def boundaryCheck(self, x, y): 
        if x <= minX or x >= (maxX - 25) or y <= (minY + 200) or y >= (maxY - 50):
            return True
        else:
            return False

    # carries out sprite movement in battle, calling enemyCheck, boundaryCheck and obstacleCheck to ensure valid movement
    def battleMovement(self, keys, obsList, enemyList): 
        tempX = self.x
        tempY = self.y
        if keys[pygame.K_a]:  
            tempX -= self.speed
        if keys[pygame.K_d]: 
            tempX += self.speed
        if keys[pygame.K_w]:  
            tempY -= self.speed
        if keys[pygame.K_s]:  
            tempY += self.speed
        # saving old position
        oldX = self.x
        oldY = self.y
        # assigning new values to x and y of sprite so they can be checked
        self.x = tempX
        self.y = tempY
        obsCollision = self.obstacleCheck(self.x, self.y, obsList) 
        boundaryCollision = self.boundaryCheck(self.x, self.y) 
        enemyCollision = self.enemyCheck(self.x, self.y, enemyList)
        if (obsCollision or enemyCollision or boundaryCollision):
            self.x = oldX
            self.y = oldY

class Tile: # needed for maze
    def __init__(self, columns, rows):
        self.columns = columns # column position of tile in the grid
        self.rows = rows # row position of tile in the grid
        self.x = self.columns * resolution # actual x position of top left corner
        self.y = self.rows * resolution # actual y position of top left corner 
        self.colour = 'cornflowerblue' # background colour of maze, as it is the colour of each tile itself (not the wall colour)
        self.rect = pygame.Rect(self.x, self.y, resolution, resolution)
        self.walls = [1,1,1,1] # array storing presence of walls starting right and going anticlockwise (1 = wall, 0 = no wall)
        self.visited = False
        self.wallMasks = [] # wall masks are involved in checking sprite collision with walls (needed to stop sprite going through the walls)

    def drawTile(self): # for drawing blank tiles of the maze, to start with
        pygame.draw.rect(display, self.colour, self.rect)

    def drawWalls(self): # for initialising walls
        # right
        if bool(self.walls[0]):
            pygame.draw.line(display, 'white',(self.x+resolution,self.y),(self.x+resolution, self.y+resolution))
        # down
        if bool(self.walls[1]):
            pygame.draw.line(display, 'white',(self.x,self.y+resolution),(self.x+resolution,self.y+resolution))
        # left
        if bool(self.walls[2]):
            pygame.draw.line(display, 'white',(self.x, self.y),(self.x,self.y+resolution))
        # up
        if bool(self.walls[3]):
            pygame.draw.line(display, 'white',(self.x, self.y),(self.x+resolution,self.y))

    def setWallMasks(self): # run only when maze generation has occurred so walls array for each tile is final
        # right
        if bool(self.walls[0]):
            wallSurface = pygame.Surface((1, resolution)) # creates surface with correct dimensions, as the wall line is 1 pixel thick and as long as the resolution
            wallSurface.fill((255, 255, 255)) # fills surface with the colour white, the same colour as the maze walls
            wallMask = pygame.mask.from_surface(wallSurface) # gets the mask itself
            self.wallMasks.append((wallMask, (self.x + resolution, self.y))) # saves mask and its location to the attribute wallMasks
        # down
        if bool(self.walls[1]):
            wallSurface = pygame.Surface((resolution, 1))
            wallSurface.fill((255, 255, 255))
            wallMask = pygame.mask.from_surface(wallSurface)
            self.wallMasks.append((wallMask, (self.x, self.y + resolution)))
        #left
        if bool(self.walls[2]):
            wallSurface = pygame.Surface((1, resolution)) 
            wallSurface.fill((255, 255, 255))
            wallMask = pygame.mask.from_surface(wallSurface)
            self.wallMasks.append((wallMask, (self.x - 1, self.y)))
        # up
        if bool(self.walls[3]):
            wallSurface = pygame.Surface((resolution, 1)) 
            wallSurface.fill((255, 255, 255))
            wallMask = pygame.mask.from_surface(wallSurface)
            self.wallMasks.append((wallMask, (self.x, self.y - 1)))

class Enemy:
    def __init__(self, enemyImg, damage, x, y):
        self.enemyImg = enemyImg
        self.damage = damage 
        self.health = 115 # default for enemies and player is 115
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(self.enemyImg) # for collision checking with other entities

    def renderEnemy(self):
        display.blit(self.enemyImg, (self.x, self.y))

    def removeHP(self, damage): 
        self.health -= damage

# this array is needed in the ShortRangeEnemy class
# if a short-range enemy collides with an object such as an obstacle or other enemy and cannot move, it will pick a vector in this list and temporarily move in that direction to get un-stuck  
directions = [(1,0), (0.707, 0.707), (0, 1), (-0.707, 0.707), (-1,0), (-0.707, -0.707), (0, -1), (0.707, -0.707)]

class ShortRangeEnemy(Enemy):
    def __init__(self, img, damage, x, y, speed):
        super().__init__(img, damage, x, y)
        self.speed = speed 
        self.vector = () # defines the direction the enemy will have to move in, either to reach the player or a temporary direction to move away from a collision-point 
        self.attackCooldown = False # if enemy is in attack cooldown, it cannot attack, this prevents continuous attack that would be too difficult. Starts as False by default
        self.attackCooldownTime = 2 # stores time left in seconds until attack cooldown is over, 2 seconds by default
        self.diversionCooldown = False # diversion cooldown indicates the enemy must temporarily move in another direction to move away from a collision-point. When false, the enemy simply moves towards the player as normal
        self.diversionCooldownTime = 5 # stores number of frames left until the diversion cooldown is over, 5 frames by default

    # calculates which direction the enemy would have to go to reach a certain entity (the player, in this case)
    def calculatePlayerDirection(self, entity): 
        x = entity.x - self.x
        y = entity.y - self.y
        if x == 0 and y == 0: # in this case, the enemy and player are in the exact same location so no movement needed 
            self.vector = (0, 0)  
            return 
        magnitude = math.sqrt(x**2 + y**2) 
        self.vector = (x / magnitude, y / magnitude) # this unit vector is the direction the enemy needs to go in

    # checks for obstacle / health bar / inventory collision to check if an enemy movement would be invalid, as enemy should not go through any of these
    def obsCollision(self, obstacleList, x, y): 
        for obstacle in obstacleList: # iterates through all obstacles to check if potential movement would cause enemy to go through any obstacles
            offset = (x - obstacle.x, y - obstacle.y)
            if (obstacle.mask.overlap(self.mask, offset)):
                return True
        if x > 225 and x < 610 and y > (maxY - 145) and y < (maxY - 50): # enemies cannot be generated in inventory area
            return True
        elif x > (maxX - 100) and y > (maxY - 265): # enemies cannot be generated in health bar area
            return True 
        else:
            return False 
    
    # checks if enemy movement would be invalid due to exceeding screen boundaries
    def boundaryCollision(self, x, y): 
        if x <= minX or x >= (maxX - 25) or y <= (minY + 200) or y >= (maxY - 50):
            return True
        else:
            return False 
        
    # checks for collision with player, in which case actions to deplete player health can occur
    def checkPlayerCollision(self, x, y, sprite):
        offset = (x - sprite.x, y - sprite.y)
        if sprite.mask.overlap(self.mask, offset):
            return True 
        else:
            return False 

    # checks for collision with other enemies, as it is not ideal if enemies can move under/over each other
    def checkEnemyCollision(self, enemyList, tempX, tempY):
        for list in enemyList:
            for enemy in list:
                if enemy != self:
                    offset = tempX - enemy.x, tempY - enemy.y
                    if enemy.mask.overlap(self.mask, offset):
                        return True
        return False 

    # if there is an obstacle block, a random direction is picked from the directions list until a valid one is found
    # diversion cooldown is set so enemy will temporarily move somewhere else 
    def offsetObstacleBlock(self, obstacleList):
        random.shuffle(directions)
        for direction in directions:
            tempX = self.x + direction[0]*self.speed*2
            tempY = self.y + direction[1]*self.speed*2
            if not self.obsCollision(obstacleList, tempX, tempY):
                self.vector = direction
                self.diversionCooldown = True 
                return True
        return False 
        
    # if there is a block due to collision with another enemy, a random direction is picked from the directions list until a valid one is found
    # diversion cooldown is set so enemy will temporarily move somewhere else 
    def offsetEnemyBlock(self, enemyList):
        random.shuffle(directions)
        for direction in directions:
            tempX = self.x + direction[0]*self.speed*2
            tempY = self.y + direction[1]*self.speed*2
            if not self.checkEnemyCollision(enemyList, tempX, tempY):
                self.vector = direction
                self.diversionCooldown = True 
                return True
        return False     
    
    def enemyMovement(self, obstacleList, sprite, enemyList):
        # first checks for diversion cooldown, in which case there is no need to move in the player's direction
        if self.diversionCooldown == True:
            self.x += self.vector[0] * self.speed
            self.y += self.vector[1] * self.speed
            return 
        # otherwise, direction for the enemy to move in is set
        self.calculatePlayerDirection(sprite) 
        # sets temporary new position of enemy, to be evaluated for collisions
        tempX = self.x + (self.vector[0]*self.speed * 5)
        tempY = self.y + (self.vector[1]*self.speed * 5)
        obstacleBlock = self.obsCollision(obstacleList, tempX, tempY)
        playerCollision = self.checkPlayerCollision(tempX, tempY, sprite)
        boundaryCollision = self.boundaryCollision(tempX, tempY)
        enemyBlock = self.checkEnemyCollision(enemyList, tempX, tempY)
        # if enemy is in contact with player and is not on attack cooldown, the sprite will have its health depleted
        if playerCollision and not(self.cooldown): 
            sprite.removeHP(self.damage)
            pygame.mixer.Sound.play(playerHitSound)
            self.cooldown = True # sets cooldown in action
        # if there is no collision, the enemy can simply move in the desired direction
        if not (obstacleBlock or playerCollision or enemyBlock or boundaryCollision): 
            self.x += self.vector[0] * self.speed
            self.y += self.vector[1] * self.speed
        # if there is an enemy or obstacle block, the relevant method to divert the enemy is called
        if obstacleBlock:
            self.offsetObstacleBlock(obstacleList)
        elif enemyBlock:
            self.offsetEnemyBlock(enemyList)
    
    def handleAttackCooldown(self, time):
        self.attackCooldownTime -= time 
        if self.attackCooldownTime <= 0:
            self.attackCooldown = False # reset cooldown
            self.attackCooldownTime = 2 # resets the time 
    
    def handleDiversionCooldown(self):
        self.diversionCooldown -= 1
        if self.cooldownTime <= 0:
            self.diversionCooldown = False
            self.cooldownTime = 5

# less functionality than ShortRange as Projectiles carry out the actual attack
class LongRangeEnemy(Enemy): 
    def __init__(self, img, damage, x, y):
        super().__init__(img, damage, x, y)

class Button: # for any different types of button I will need to create in my program
    def __init__(self, x, y, width, height, img, hoverImg):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
        self.hoverImg = hoverImg
        self.flag = False # all buttons have a flag - when button is pressed, flag changes, and an event is triggered
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def checkClick(self, event): # evaluates whether the user clicked specifically on a button and toggles the flag to signify a button click
        mouse_pos = event.pos
        if self.rect.collidepoint(mouse_pos) and event.button == 1:
            self.flag = True 
            pygame.mixer.Sound.play(clickSound) 

    def renderButton(self): # renders button based on whether it is being hovered over
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y): # checks for mouse collision with button, but no click yet
            display.blit(self.hoverImg, (self.x, self.y)) # display hover image if mouse is hovering over button
        else:
            display.blit(self.img, (self.x, self.y)) # display normal button image otherwise
     
    def resetButton(self): # resets the button as though it has not been pressed so it can be reused
        self.flag = False 

class MoneyCount:
    def __init__(self, imageList):
        self.value = 0 # initially set to 0, it gets incremented during the game when gems are collected
        self.imageList = imageList # list of images that will be needed to display the amount of money in the correct font, using imported images
        self.x = maxX * 0.85 # starting x position of money count on the screen
        self.y = 0 # # y position of money count - located at the top of the screen
        self.width = 100 
        self.height = 20

    def renderMoney(self):  
        valueString = str(self.value)
        xPos = self.x # saving the original starting value of x as it will be incremented each time so each number is next to the previous one
        # first I need to clear the area around the money so it can be re-rendered without layering over digits and displaying the wrong number
        money_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        display.fill('white', money_rect)
        display.blit(self.imageList[10], (xPos, self.y))
        xPos += 20
        for digit in valueString: # iterates through each digit of the value
            digitImg = self.imageList[int(digit)] # gets the appropriate image representing that digit, using indexing (list contains images of 0-9 in that order)
            display.blit(digitImg, (xPos, self.y)) # draws image onto screen
            xPos += 20 # increments x position so each number is next to the previous one - each digit is going to be scaled to a width of 20 pixels

    def incrementValue(self, moneyReceived): 
        self.value += moneyReceived
        self.renderMoney()

    def decrementValue(self, moneyLost): 
        self.value -= moneyLost
        self.renderMoney()

# instantiation of money count so I can use it in other files
moneyCount = MoneyCount(numListImgs)

font = pygame.font.Font('freesansbold.ttf', 70) 
def setCountdown(): # needed for rendering the countdown in the maze and battle
    countdownNums = ['3', '2', '1', 'GO!'] # this is all the text that needs to be displayed for the countdown
    for item in countdownNums:
        countdownText = font.render(item, True, (255,255,255)) # creates text object to be rendered
        countdownTextRect = countdownText.get_rect() # defines area of text
        countdownTextRect.center = (maxX*0.5, maxY*0.5) # positions the text
        displayBox = pygame.Rect(maxX*0.5 - 100, maxY*0.5 - 90, 200, 200) # defines the box that the text is placed on
        pygame.draw.rect(display, 'blue', displayBox) # draws the box that the text is placed on
        display.blit(countdownText, countdownTextRect) # draws the text, must be on top of the box
        time.sleep(1) # delay as part of the countdown
        pygame.display.flip() # updates screen

class Gemstone:
    def __init__(self, gem_img, x, y, value):
        self.gem_img = gem_img
        self.x = x
        self.y = y
        self.value = value
        self.mask = pygame.mask.from_surface(self.gem_img) # for collision checking with sprite, needed for sprite to collect gemstones

    def getValue(self): 
        return self.value 
    
    def renderGem(self):
        display.blit(self.gem_img, (self.x, self.y))

    def gemCheck(self, sprite): # used to check if a player is in contact with a gem to signify a player has collected it
        offset = (self.x - sprite.x), (self.y - sprite.y) 
        if sprite.mask.overlap(self.mask, (offset)): 
            return True
        
class Inventory:
    def __init__(self, img, startingX, y, invSlotSize):
        # slot attributes will each contain a list of data relevant to the slot
        self.slot0 = [0, None]
        self.slot1 = [0, None]
        self.slot2 = [0, None]
        self.slot3 = [0, None]
        self.slot4 = [0, None]
        self.slot5 = [0, None]
        self.mainInventory = [self.slot0, self.slot1, self.slot2, self.slot3, self.slot4, self.slot5]
        self.img = img # blank image of the inventory by default; it is the same for all slots
        self.startingX = startingX # x position of slot0, following slots will be a fixed distance apart from the previous one
        self.y = y # the y coordinate of all inventory images, as they are all going to be in a horizontal line at the bottom
        self.invSlotSize = invSlotSize # the length of the slot, useful for displaying things on the screen 
        self.pointer = 0 # points to next free slot
        self.weaponInUse = None # weapon in the highlighted inventory slot

    def setSlotRects(self): # defines area of each inventory slot
        x = self.startingX
        for slot in self.mainInventory: # allows me to access each slot in turn
            rect = pygame.Rect(x, self.y, self.invSlotSize, self.invSlotSize) # making a rectangle so that if a slot is clicked, this can be registered
            slot.append(rect) # adding to the slot, which is a list of data about the slot
            x += self.invSlotSize # to ensure each rect is next to the previous one, not on top 
    
    def render_inventory(self):
        posX = self.startingX
        for slot in self.mainInventory:
            display.blit(self.img, (posX, self.y)) # draws the empty slot
            if slot[0]: # slot[0] is either 0 or 1, so either not filled or filled, if it is 1, ie. filled, then draw weapon too
                # slot[1] is an object, it is the weapon object
                slot[1].renderWeapon(posX+(self.invSlotSize/4), self.y+(-10+self.invSlotSize/4))
            posX += self.invSlotSize # ensures each slot is placed directly adjacent to the previous one

    def addPointer(self): # pointer refers to the next free inventory space 
        self.pointer +=1
        if self.pointer > 5:
            self.pointer = None # ie. all spaces filled now

    def fill_inventory(self, weaponsList, index): # ie if a weapon is bought, add it to inventory
        currentSlot = self.mainInventory[self.pointer] # get next free slot which can now be used for storing a weapon
        currentSlot[0] = 1 # modifies current slot so it is now filled
        currentSlot[1] = weaponsList[index] # actually fills the current slot with the desired weapon
        self.addPointer() # increments pointer  
    
    def setCurrentWeapon(self, index): # make this weapon the current one if clicked on
        slot = self.mainInventory[index] # gets the slot of the current weapon
        self.weaponInUse = slot[1] # assigns current weapon

    def highlightSlot(self, slotRect): # must be repeated every time inventory is rendered in battle part of game
        pygame.draw.line(display, (0,0,0), (slotRect.x, slotRect.y), (slotRect.x+self.invSlotSize, slotRect.y), width=5) # top border
        pygame.draw.line(display, (0,0,0), (slotRect.x, slotRect.y), (slotRect.x, slotRect.y+self.invSlotSize), width=5) # left border
        pygame.draw.line(display, (0,0,0), (slotRect.x+self.invSlotSize, slotRect.y), (slotRect.x+self.invSlotSize, slotRect.y+self.invSlotSize), width=5) 
        # right border
        pygame.draw.line(display, (0,0,0), (slotRect.x, slotRect.y+self.invSlotSize), (slotRect.x+self.invSlotSize, slotRect.y+self.invSlotSize), width=5) 
        # bottom border

userInventory = Inventory(invSlotImg, 250, maxY - 100, invSlotSize) 
userInventory.setSlotRects() # needed to initialise inventory slots

class ShopWeapon:
    def __init__(self, price, static_img, alt_img, x, y):
        self.price = price
        self.static_img = static_img # image when it is available to be bought
        self.alt_img = alt_img # image when it is unavailable to be bought
        self.x = x
        self.y = y
        self.bought = False # to begin with all weapons have to start out as False, ie. not bought yet

    def updateBought(self):
        if self.bought == False: # the main use of this function is to set an item to bought=True once it has been purchased
            self.bought = True 

    def checkPrice(self, value): # moneyCount would be passed in to check if the item is affordable for the user 
        if value - self.price >= 0: 
            return True
        else:
            return False 

    def render_img(self, priceCheck): # renders the correct image of the weapon based on if the player can afford it 
        if priceCheck:
            display.blit(self.static_img, (self.x, self.y))
        else:
            display.blit(self.alt_img, (self.x, self.y))
    
class Weapon: # for actual weapons rather than just weapons in inventory
    def __init__(self, damage, inventory_img): # one image is to show up in inventory, one image is so the weapon appears when using it in battle
        self.damage = damage
        self.inventory_img = inventory_img
        self.vector = () # specifies direction that the weapon will be used in
    
    def getDamage(self): 
        return self.damage 

    def renderWeapon(self, x, y):
        display.blit(self.inventory_img, (x,y))

class ShortRangeWeapon(Weapon): 
    def __init__(self, damage, inventory_img, weapon_img):
        super().__init__(damage, inventory_img)
        self.weapon_img = weapon_img
        self.cooldown = False # false by default, used so that when a sword animation is occurring, other weapons cannot be simultaneously used
        self.mask = pygame.mask.from_surface(self.weapon_img)
        self.angleLB = 0 # lower bound for weapon swinging animation
        self.angleUB = 0 # upper bound for weapon swinging animation

    def getDirection(self, mouseX, mouseY, playerX, playerY):
        # uses direction of click to produce a direction that the weapon should be aimed in
        x = mouseX - playerX
        y = mouseY - playerY
        if x == 0 and y == 0:
            self.vector = (0, 0)
            return 
        magnitude = math.sqrt(x**2 + y**2)
        self.vector = (x / magnitude, y / magnitude)  

    def setUpWeapon(self): # creates an angle range for the weapon to be swung in
        x = self.vector[0]
        y = self.vector[1]
        angle = math.degrees(math.atan2(-y, x)) # -y and  x aligns the weapon correctly in the right direction
        angle = int((angle + 360) % 360) # normalises it so it is within range 0 to 360
        self.angleLB = angle - 15
        self.angleUB = angle + 15
        self.cooldown = True # cooldown as a weapon cannot be used while the weapon swinging animation is already occurring
    
    def useWeapon(self, sprite, enemyList): # this will run in the main loop 
        if self.cooldown == True:
            copyImg = pygame.transform.rotate(self.weapon_img, self.angleLB) # saves a version of the image for rotations/animation
            display.blit(copyImg, (sprite.x - 15, sprite.y - 15)) # positions the weapon next to the player
            self.angleLB += 10 # angle is incremented every time this method is run so the weapon rotates in real-time on the screen
            # every time the weapon rotates, a check for a collision with each enemy needs to occur, so the weapon can decrement enemy health if appropriate
            if self.angleLB >= self.angleUB: # checks whether animation is done now 
                self.cooldown = False # i.e. weapon is done being used, so player is free to use it again once the loop has terminated
            for list in enemyList:
                for enemy in list:
                    offset = (sprite.x - enemy.x, sprite.y - enemy.y)
                    if (enemy.mask.overlap(self.mask, offset)):
                        pygame.mixer.Sound.play(enemyHitSound)
                        enemy.removeHP(self.damage)
                        return 
        
class LongRangeWeapon(Weapon):
    def __init__(self, damage, inventory_img):
        super().__init__(damage, inventory_img)

# instantiation of weapon so it can be used in the relevant files
swordI = ShortRangeWeapon(5, swordI_icon, swordI_actualImg) 
swordII = ShortRangeWeapon(10, swordII_icon, swordII_actualImg)
swordIII = ShortRangeWeapon(15, swordIII_icon, swordIII_actualImg)
pistol = LongRangeWeapon(20, pistol_icon)
bow = LongRangeWeapon(25, bow_icon)
flameBow = LongRangeWeapon(30, flameBow_icon)
weaponsList = [swordI, swordII, swordIII, pistol, bow, flameBow]

class Obstacle:
    def __init__(self, x, y, img): 
        self.x = x
        self.y = y
        self.obstacleImg = img
        self.mask = pygame.mask.from_surface(self.obstacleImg)
    
    def renderObstacle(self):
        display.blit(self.obstacleImg, (self.x, self.y))

class Projectile:
    def __init__(self, x, y, projectileImg, speed, damage):
        self.x = x
        self.y = y
        self.projectileImg = projectileImg 
        self.speed = speed
        self.damage = damage
        self.mask = pygame.mask.from_surface(self.projectileImg) # mask for projectile allows checking for collision with obstacles, player, enemies, etc. 
        self.vector = () # the vector representing the trajectory of the projectile
        self.finished = False # flag to check if projectile has run its course, must begin as False

    def renderProjectile(self):
        display.blit(self.projectileImg, (self.x, self.y))

    def obstacleCollision(self, x, y, obstacleList): # method belongs to parent class as both enemy and player projectiles are affected by obstacle / inventory / health bar collision
        for obstacle in obstacleList: # iterates through all obstacles to check if projectile would collide with any obstacle
            offset = (x - obstacle.x, y - obstacle.y)
            if (obstacle.mask.overlap(self.mask, offset)):
                return True 
        if x > 225 and x < 610 and y > (maxY - 145) and y < (maxY - 50): # projectiles should disappear if they hit the inventory
            return True 
        if x > (maxX - 100) and y > (maxY - 265): # projectiles should disappear if they hit the health bar 
            return True  
        return False 

    def setTrajectory(self, xPos, yPos): # xPos and yPos may be an entity's coordinates (player or enemy) or coordinates of user click
        x = xPos - self.x
        y = yPos - self.y
        if x == 0 and y == 0:
            self.vector = (0, 0)  
            return 
        magnitude = math.sqrt(x**2 + y**2)
        self.vector = (x / magnitude, y / magnitude)
    
    def boundaryCollision(self, x, y): # if projectile exceeds screen boundaries then it has run its course
        if x <= minX or x >= (maxX - 25) or y <= (minY + 200) or y >= (maxY - 50):
            return True 
        else:
            return False 

class EnemyProjectile(Projectile):
    def __init__(self, x, y, projectileImg, speed, damage):
        super().__init__(x, y, projectileImg, speed, damage)
        self.time = random.uniform(1,3) # generates float value which is the time after which the projectile will become active
        self.startingX = 0 
        self.startingY = 0

    def saveStartingPos(self): # this binds an EnemyProjectile to its corresponding long-range enemy and allows it to reset from the same position 
        self.startingX = self.x
        self.startingY = self.y

    def checkPlayerCollision(self, sprite, x, y): # needed so HP can be removed from the player as appropriate 
        offset = (x - sprite.x, y - sprite.y)
        if sprite.mask.overlap(self.mask, offset):
            return True 
        else:
            return False 
    
    def moveProjectile(self, sprite, obstacleList): 
        tempX = self.x + self.vector[0]*self.speed 
        tempY = self.y + self.vector[1]*self.speed 
        playerCollision = self.checkPlayerCollision(sprite, tempX, tempY)
        if not (playerCollision or self.boundaryCollision(tempX, tempY) or self.obstacleCollision(tempX, tempY, obstacleList)):
            # sets projectile x and y position as long as there are no collisions 
            self.x = tempX 
            self.y = tempY
        else:
            self.finished = True # if there is a collision, the projectile should be flagged as finished
            if playerCollision: # this is the only situation where an additional action needs to be taken beyond setting self.finished = True
                pygame.mixer.Sound.play(playerHitSound)
                sprite.removeHP(self.damage) 

    def resetProjectile(self): # sends projectile back to the enemy so it can be fired again
        self.time = random.uniform(1,3) # assigns the projectile a new countdown to allow for unpredictability regarding when an enemy will shoot
        self.finished = False # so it is an inactive projectile again
        self.x = self.startingX
        self.y = self.startingY

        
class PlayerProjectile(Projectile):
    def __init__(self, x, y, projectileImg, speed, damage):
        super().__init__(x, y, projectileImg, speed, damage)
        self.angle = 0 # angle of rotation of the projectile to fire in the right direction, 0 by default

    def rotateProjectile(self): # rotates projectile image to be fired in the correct direction
        x = self.vector[0]
        y = self.vector[1]
        angle = math.degrees(math.atan2(y, x)) 
        self.angle = (angle + 360) % 360 # normalises it so it is within range 0 to 360
        self.projectileImg = pygame.transform.rotate(self.projectileImg, -self.angle)

    def enemyCollision(self, enemyList): # note a projectile can only attack one enemy before it dies out, can't attack multiple
        for list in enemyList:
            for enemy in list:
                offset = (self.x - enemy.x, self.y - enemy.y)
                if enemy.mask.overlap(self.mask, offset):
                    pygame.mixer.Sound.play(enemyHitSound)
                    enemy.removeHP(self.damage)
                    return True # returns immediately so projectile only affects one enemy max.

    def moveProjectile(self, obstacleList, enemyList):
        tempX = self.x + self.vector[0]*self.speed
        tempY = self.y + self.vector[1]*self.speed
        collision = self.enemyCollision(enemyList) # checks for any enemy collisions, but removal of enemy health points happens outside of this method, in the enemyCollision method instead
        if collision or self.obstacleCollision(tempX, tempY, obstacleList) or self.boundaryCollision(tempX, tempY):
            self.finished = True 
        else:
            self.x = tempX
            self.y = tempY

sprite = Character(resolution*3+4, resolution*3+4, 2, spriteImg)


