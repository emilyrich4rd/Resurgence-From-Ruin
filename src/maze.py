# file for maze-related code, including maze generation and gemstone generation

import pygame
pygame.init()

import random
from random import randint # check if it is redundant if i already imported random? but seems to be bringing up an error if i don't do this as well
from gameData import *
from soundFile import *
from imageData import *
from intro import *

# dimensions for generating the maze specifically, as the maze will not occupy the entire screen
x = dimensions[0] - 3
y = dimensions[1] - 3
dims = (x, y)

# function to get neighbours of a particular maze tile
def getNeighbours(grid, ct):
    neighbours = []
    # right neighbours
    if ct.columns < dims[0]-1 and not grid[ct.rows-3][ct.columns-2].visited:
        neighbours.append(grid[ct.rows-3][ct.columns-2])
    # down neighbours
    if ct.rows < dims[1]-1 and not grid [ct.rows-2][ct.columns-3].visited:
        neighbours.append(grid[ct.rows-2][ct.columns-3])
    # left neighbours
    if ct.columns > 3 and not grid[ct.rows-3][ct.columns-4].visited:
        neighbours.append(grid[ct.rows-3][ct.columns-4])
    # up neighbours
    if ct.rows > 3 and not grid[ct.rows-4][ct.columns-3].visited:
        neighbours.append(grid[ct.rows-4][ct.columns-3])
    return neighbours

# all maze tiles begin with 4 walls, this subroutine is needed to remove some walls based on the particular maze generation
def removeWalls(ct, chosen):
    # right
    if chosen.columns - ct.columns > 0:
        ct.walls[0] = 0
        chosen.walls[2] = 0
    # down
    if chosen.rows - ct.rows > 0:
        ct.walls[1] = 0
        chosen.walls[3] = 0
    # left 
    if chosen.columns - ct.columns < 0:
        ct.walls[2] = 0
        chosen.walls[0] = 0
    # up
    if chosen.rows - ct.rows < 0:
        ct.walls[3] = 0
        chosen.walls[1] = 0

# subroutine to generate a particular maze design
def generateMaze(grid, ct):
    stack = []
    complete = False  # flag to track if maze is complete yet
    while not complete:
        validNeighbours = getNeighbours(grid, ct)
        if len(validNeighbours) > 0:
            # selects random neighbour and incorporates it into the maze
            chosen = random.choice(validNeighbours) 
            removeWalls(ct, chosen) 
            chosen.visited = True
            stack.append(ct)
            ct = chosen
        else:
            if len(stack) > 0:
                ct = stack.pop()
            else:
                complete = True  # when the stack is empty, flag is set to True to terminate loop

restrictedCoords = [] # gem coordinates are stored in here so every time a new gem is generated, another cannot be generated in the exact same location

# setQuartz, setJade, setSapphire, setRuby and setDiamond (see below) are all similar functions which generate these gem types in random locations in the maze
# each function returns a list of that gem type so they can be easily kept track of

def setQuartz(num): # num is the total number of gemstones
    quartzNum = int(0.4*num) # 40% of total gems are quartz
    quartzGems = []
    for i in range(quartzNum): 
        validCoords = False
        while validCoords == False: # set of coordinates is repeatedly generated until valid
            x = randint(4*resolution, (dims[0]-1) * resolution-1) 
            y = randint(4*resolution, (dims[1]-1) * resolution-1) 
            coordPair = (x,y) 
            if coordPair not in restrictedCoords: # unique position for gem has been found
                validCoords = True 
                restrictedCoords.append(coordPair) 
        # instantiate new quartz object
        quartz = Gemstone(quartzImg, x,y, 5) 
        quartzGems.append(quartz)
    return quartzGems 

def setJade(num): # num is the total number of gemstones
    jadeNum = int(0.25*num) # 25% of total gems are jade
    jadeGems = []
    for i in range(jadeNum): 
        validCoords = False
        while validCoords == False: # set of coordinates is repeatedly generated until valid
            x = randint(4*resolution, (dims[0]-1) * resolution-1) 
            y = randint(4*resolution, (dims[1]-1) * resolution-1)
            coordPair = (x,y) 
            if coordPair not in restrictedCoords: # unique position for gem has been found
                validCoords = True 
                restrictedCoords.append(coordPair) 
        # instantiate new jade object
        jade = Gemstone(jadeImg, x,y, 8)
        jadeGems.append(jade)
    return jadeGems 

def setSapphire(num): # num is the total number of gemstones
    sapphireNum = int(0.2*num) # 20% of gems are sapphires
    sapphireGems = []
    for i in range(sapphireNum): 
        validCoords = False
        while validCoords == False: # set of coordinates is repeatedly generated until valid
            x = randint(4*resolution, (dims[0]-1) * resolution-1) 
            y = randint(4*resolution, (dims[1]-1) * resolution-1) 
            coordPair = (x,y) 
            if coordPair not in restrictedCoords: # unique position for gem has been found
                validCoords = True 
                restrictedCoords.append(coordPair) 
        # instantiate new sapphire object
        sapphire = Gemstone(sapphireImg, x,y, 12) 
        sapphireGems.append(sapphire)
    return sapphireGems 

def setRuby(num): # num is the total number of gemstones
    rubyNum = int(0.1*num) # 10% of gems are rubies
    rubyGems = []
    for i in range(rubyNum): 
        validCoords = False
        while validCoords == False: # set of coordinates is repeatedly generated until valid
            x = randint(4*resolution, (dims[0]-1) * resolution-1) 
            y = randint(4*resolution, (dims[1]-1) * resolution-1)
            coordPair = (x,y) 
            if coordPair not in restrictedCoords: # unique position for gem has been found
                validCoords = True 
                restrictedCoords.append(coordPair) 
        # instantiate new ruby object
        ruby = Gemstone(rubyImg, x,y, 15)
        rubyGems.append(ruby)
    return rubyGems 

def setDiamond(num): # num is the total number of gemstones
    diamondNum = int(0.05*num) # 5% of gems are diamonds
    diamondGems = []
    for i in range(diamondNum):
        validCoords = False
        while validCoords == False: # set of coordinates is repeatedly generated until valid
            x = randint(4*resolution, (dims[0]-1) * resolution-1) 
            y = randint(4*resolution, (dims[1]-1) * resolution-1) 
            coordPair = (x,y) 
            if coordPair not in restrictedCoords: # unique position for gem has been found
                validCoords = True 
                restrictedCoords.append(coordPair) 
        # instantiate new diamond object
        diamond = Gemstone(diamondImg, x,y, 20)
        diamondGems.append(diamond)
    return diamondGems 

# iterating through grid to draw each tile and then each wall of the maze
def drawMaze(grid):
    for tileRow in grid:
        for tile in tileRow:
            tile.drawTile()
            tile.drawWalls()

# iterating through list of all gems and draws each into the maze
def drawGems(gemLists):
    for list in gemLists:
        for gem in list:
            gem.renderGem()

# function to generate and return a list of all gemstones
def setGems(randomGems):
    quartzList = setQuartz(randomGems)
    jadeList = setJade(randomGems)
    sapphireList = setSapphire(randomGems)
    rubyList = setRuby(randomGems)
    diamondList = setDiamond(randomGems)
    return [quartzList, jadeList, sapphireList, rubyList, diamondList]

# allows maze walls to be detected so the player does not go through them, by setting a mask for each
def setMasks(grid): 
    for tilerow in grid:
        for tile in tilerow:
            tile.setWallMasks()
        
# moves the sprite in the maze based on what key they pressed
def userCheck(grid): 
    keys = pygame.key.get_pressed()
    sprite.mazeMovement(keys, grid)

# sets up gems and places sprite in the maze
def setUpMaze(randomGems): 
    allGems = setGems(randomGems)
    sprite.setStartPos(resolution*3+4, resolution*3+4)
    sprite.setSpeed(4)
    sprite.resize(20, 30)
    return allGems

# sets/resets the maze by calling the relevant functions, ensuring the maze is different each time it is played
def resetMaze():
    grid = []
    for row in range(3, dims[1]):
        tileRow = []
        for column in range(3, dims[0]):
            tile = Tile(column, row)
            tileRow.append(tile)
        grid.append(tileRow)
    ct = grid[0][0]
    ct.visited = True
    generateMaze(grid, ct)
    setMasks(grid)
    return grid

# handles events when player comes into contact with a gemstone
def gemCollection(allGems): 
    for list in allGems:
        for gem in list:
            gemCollected = gem.gemCheck(sprite)
            if gemCollected: # if player is in contact with a gem, it is registered as collected and removed from existence
                pygame.mixer.Sound.play(gemCollectedSound)
                gemValue = gem.getValue()
                moneyCount.incrementValue(gemValue)
                list.remove(gem) 

# checks if all gems have been collected ie. maze is complete
def checkGameEnd(allGems): 
    end = True
    for list in allGems: # checks if all gem lists are empty, so all gems have been collected
        if not(list == []): 
            end = False
    return end 

# back button for returning to menu
xPos = 30 
yPos = 50
backButton = Button(xPos, yPos, 20, 20, backButtonImg, backButtonHoverImg)

# summarises maze subroutines for convenience, useful when calling in main.py
def mazeFunctions(grid, allGems): 
    setBG(mazeBackgroundImg)
    drawMaze(grid) 
    drawGems(allGems)
    userCheck(grid)
    sprite.renderSprite() 
    moneyCount.renderMoney()
    gemCollection(allGems)
    backButton.renderButton()
    pygame.display.flip()      

# buttons displayed when maze is complete
playAgain = Button(maxX*0.25, maxY*0.5, 100, 75, mazeButtonImgs[0], mazeButtonImgs[1])
quitMaze = Button(maxX*0.6, maxY*0.5, 100, 75, mazeButtonImgs[2], mazeButtonImgs[3])

# displays outcome and relevant buttons once maze is complete
def setEndMaze(): 
    setBG(mazeEndBG)
    playAgain.renderButton()
    quitMaze.renderButton()
    





