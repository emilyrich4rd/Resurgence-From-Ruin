# this file handles the main game logic and switching between different game states

import pygame
pygame.init()
import time

from gameData import *
from maze import * 
from intro import *
from shop import * 
from battle import *
from progressTracker import *
from soundFile import *
from imageData import *

running = True
inGame = False 
maze = False
progressTracker = False
shop = False
battle = False 
mazeJustQuit = False

while running:
    level = 1
    damageScore = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
    if not startButton.flag: # if the start button hasn't been clicked yet, the start screen is rendered instead each frame
        runStartScreen(gameStartImg, startButton)
        if event.type == pygame.MOUSEBUTTONDOWN: # repeatedly checks if the start button has been pressed 
            startButton.checkClick(event)
    else: # this condition is satisfied once the start button has been pressed
        if not goToMenu.flag: # if the go to menu button hasn't been rendered yet, the backstory screen is rendered instead each frame
            setBackstory(backstoryImg, goToMenu)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    goToMenu.checkClick(event)
        else: #  ie. goToMenu button has been pressed, we can now go to the main game
            inGame = True # inGame flag allows the main game to run (terminates if overall game won/loss, so inGame is set to False at that point)
            while inGame:
                while not (maze or battle or progressTracker or shop): # ie not on one of the other playing modes, so must be on the in game menu 
                    renderMenu(menuBG, shopButton, mazeButton, progressTrackerButton, battleButton)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            pygame.quit()
                            exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # this time, there are 4 buttons, so a click could correspond to any one of 4 possible buttons
                            mazeButton.checkClick(event)
                            while mazeButton.flag == True:
                                maze = True
                                display.fill((0,0,0)) # clear screen to get rid of menu
                                randomGems = randint(25, 60)
                                allGems = setUpMaze(randomGems)
                                grid = resetMaze()
                                mazeFunctions(grid, allGems) # shows how the maze looks before countdown
                                setCountdown()
                                while maze:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            running = False
                                            pygame.quit()
                                            exit()
                                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            backButton.checkClick(event)
                                            if backButton.flag == True:
                                                maze = False 
                                                mazeButton.resetButton()
                                                backButton.resetButton()
                                    mazeFunctions(grid, allGems)
                                    if checkGameEnd(allGems):
                                        time.sleep(1) # so the game does not end abruptly
                                        pygame.mixer.Sound.play(mazeCompleteSound)
                                        clicked = False # flag to check if 'play again' or 'quit game' button has been clicked
                                        while not clicked: # display these buttons when nothing has been clicked yet 
                                            for event in pygame.event.get():
                                                setEndMaze()
                                                pygame.display.flip()
                                                if event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    exit()
                                                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                                    playAgain.checkClick(event)
                                                    quitMaze.checkClick(event)
                                                    if playAgain.flag:
                                                        clicked = True
                                                        maze = False 
                                                        playAgain.resetButton()
                                                        pygame.event.clear() 
                                                        time.sleep(0.05)
                                                    elif quitMaze.flag:
                                                        clicked = True
                                                        maze = False
                                                        mazeButton.resetButton()
                                                        mazeJustQuit = True
                                                        print(battleButton.flag)
                                                        quitMaze.resetButton()
                                                        pygame.event.clear() 
                                                        time.sleep(0.05)
                                                
                            shopButton.checkClick(event)
                            if shopButton.flag == True:
                                shop = True
                                display.fill(('darkblue')) # clear screen to get rid of menu
                                while shop == True:
                                    for event in pygame.event.get():
                                        initialiseShop(shopWeaponsList, moneyCount, buttonList)
                                        if event.type == pygame.QUIT:
                                            running = False
                                            pygame.quit()
                                            exit()
                                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            runShop(mouse_x, mouse_y, buttonList, shopWeaponsList, moneyCount, userInventory, weaponsList)
                                            backButton.checkClick(event)
                                            if backButton.flag == True:
                                                shop = False 
                                                shopButton.resetButton()
                                                backButton.resetButton()
                            progressTrackerButton.checkClick(event)
                            if progressTrackerButton.flag == True:
                                progressTracker = True # allows game to be in the progress tracker component until otherwise specified 
                                while progressTracker == True:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            running = False
                                            pygame.quit()
                                            exit()
                                        drawProgressTracker(level, damageScore) # draws progress tracker onto screen
                                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                            backButton.checkClick(event) # repeatedly checks if user has clicked to go back to menu
                                        if backButton.flag == True: 
                                            progressTracker = False # so screen goes back to in game menu
                                            # statements below reset buttons to be clicked again in the future
                                            progressTrackerButton.resetButton()
                                            backButton.resetButton()  
                            battleButton.checkClick(event)
                            if mazeJustQuit == True: # battle button and quit maze are in the same location so without this, pressing quit maze might accidentally active battle button to begin battle
                                battleButton.resetButton()
                                mazeJustQuit = False # resets this flag if used again
                            while battleButton.flag == True:
                                battle = True
                                selectedSlot = None
                                playerProjectileList = []
                                display.fill(('#040B68'))
                                levelData = setLevel(level) 
                                obstacleList = setObstacles(levelData) 
                                enemyList = setEnemies(baseAttack, level, obstacleList) 
                                initialiseSprite(obstacleList) 
                                inactiveProjectiles = setProjectiles(enemyList) 
                                activeProjectiles = [] 
                                setBattle(levelData, obstacleList, startingX, startingY, height, enemyList)
                                renderEnemies(enemyList, activeProjectiles, inactiveProjectiles)
                                setCountdown()
                                while battle == True:
                                    gameTime = clock.tick(60) / 1000.0
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            running = False
                                            pygame.quit()
                                            exit() # ensures that if user quits pygame window, it will actually be removed
                                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                            weaponFired = checkWeaponClick(event, userInventory)
                                            if not weaponFired: # click must have been on inventory
                                                selectedSlot = getSlot(event, userInventory)
                                            if weaponFired: # basically just checks if a click occurred that wasn't on the inventory
                                                fireWeapon(event, userInventory, playerProjectileList)
                                    setBattle(levelData, obstacleList, startingX, startingY, height, enemyList)
                                    if selectedSlot != None: # prevents highlighting at the start when no slot is chosen
                                        userInventory.highlightSlot(selectedSlot[2])
                                    if userInventory.weaponInUse == swordI or userInventory.weaponInUse == swordII or userInventory.weaponInUse == swordIII:
                                        userInventory.weaponInUse.useWeapon(sprite, enemyList)
                                    allEnemyHandling(enemyList, gameTime, activeProjectiles, inactiveProjectiles, obstacleList)
                                    handleWeaponProjectiles(playerProjectileList, obstacleList, enemyList)
                                    print(sprite.x, sprite.y)
                                    pygame.display.flip()
                                    endGame = checkEndGame(enemyList)
                                    if endGame:
                                        endGame = False # resets endGame so this can be checked again
                                        if battleWon():
                                            level += 1
                                        else:
                                            damageScore += 1
                                        if level > 5: # ends entire game
                                            pygame.mixer.Sound.play(gameWonSound)
                                            game = True
                                            while game:
                                                setBG(gameWonImg)
                                                for event in pygame.event.get():
                                                    if event.type == pygame.QUIT:
                                                        running = False
                                                        pygame.quit()
                                                        exit()
                                                pygame.display.flip()
                                        elif damageScore > 5: # ends entire game
                                            pygame.mixer.Sound.play(gameLostSound)
                                            game = True
                                            while game:
                                                setBG(gameLostImg)
                                                for event in pygame.event.get():
                                                    if event.type == pygame.QUIT:
                                                        running = False
                                                        pygame.quit()
                                                        exit()
                                                pygame.display.flip()
                                        else: # entire game has not terminated yet 
                                            buttonSelected = False
                                            if battleWon():
                                                pygame.mixer.Sound.play(battleWonSound) 
                                            else:
                                                pygame.mixer.Sound.play(battleLostSound)
                                        while not(buttonSelected): # end battle screen runs until a button is clicked
                                            if battleWon():
                                                setBG(battleWonImg)
                                            else: 
                                                setBG(battleLostImg)
                                            # regardless of battle outcome, same buttons are rendered
                                            playBattle.renderButton()
                                            quitBattle.renderButton()
                                            pygame.display.flip()
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    running = False
                                                    pygame.quit()
                                                    exit()
                                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                                    # checks if either button was clicked
                                                    playBattle.checkClick(event)
                                                    quitBattle.checkClick(event)
                                                if playBattle.flag == True: # allows user to keep playing
                                                    buttonSelected = True
                                                    playBattle.resetButton()
                                                    battle = False 
                                                    pygame.event.clear() 
                                                    time.sleep(0.05)
                                                    # battleButton.resetButton() is not included here so game stays in battle 
                                                elif quitBattle.flag == True: # allows user to go back to menu 
                                                    buttonSelected = True 
                                                    quitBattle.resetButton()
                                                    battleButton.resetButton()
                                                    battle = False 
                                                    pygame.event.clear() 
                                                    time.sleep(0.05)
                                   
                                        

    
                                      
                            
                    

       



