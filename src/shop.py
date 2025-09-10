# file for shop interface-related code 

import pygame
pygame.init()

# importing other files here
from gameData import * 
from soundFile import *
from imageData import *
from maze import *

# instantiation of shopWeapons (S indicates they are only for display in the shop) 
swordI_S = ShopWeapon(100, shopImgList[0], shopImgList[1], maxX*0.1, maxY*0)
swordII_S = ShopWeapon(150, shopImgList[2], shopImgList[3], maxX*0.1, maxY*0.15)
swordIII_S = ShopWeapon(200, shopImgList[4], shopImgList[5], maxX*0.1, maxY*0.3)
pistol_S = ShopWeapon(250, shopImgList[6], shopImgList[7], maxX*0.1, maxY*0.45)
bow_S = ShopWeapon(300, shopImgList[8], shopImgList[9], maxX*0.1, maxY*0.6)
flameBow_S = ShopWeapon(350, shopImgList[10], shopImgList[11], maxX*0.1, maxY*0.75)

# list of all shop weapon objects so that they can easily be referred to and all items can be iterated through
shopWeaponsList = [swordI_S, swordII_S, swordIII_S, pistol_S, bow_S, flameBow_S] 

# instantiation of a purchase button for each item, which will only be rendered if item.bought == False as below, showing these items are available to be bought
purchase0 = Button(maxX*0.6, maxY*0.05, purchaseButtonWidth, purchaseButtonHeight, purchaseButton_img, purchaseButton_hoverImg)
purchase1 = Button(maxX*0.6, maxY*0.2, purchaseButtonWidth, purchaseButtonHeight, purchaseButton_img, purchaseButton_hoverImg)
purchase2 = Button(maxX*0.6, maxY*0.35, purchaseButtonWidth, purchaseButtonHeight, purchaseButton_img, purchaseButton_hoverImg)
purchase3 = Button(maxX*0.6, maxY*0.5, purchaseButtonWidth, purchaseButtonHeight, purchaseButton_img, purchaseButton_hoverImg)
purchase4 = Button(maxX*0.6, maxY*0.65, purchaseButtonWidth, purchaseButtonHeight, purchaseButton_img, purchaseButton_hoverImg)
purchase5 = Button(maxX*0.6, maxY*0.8, purchaseButtonWidth, purchaseButtonHeight, purchaseButton_img, purchaseButton_hoverImg)

# list of purchase buttons so they can easily be rendered using iteration through the list
buttonList = [purchase0, purchase1, purchase2, purchase3, purchase4, purchase5]

# displays shop
def initialiseShop(weaponList, moneyCount, buttonList): 
    moneyCount.renderMoney() # shows amount of money so user knows how much they have
    for item in weaponList: 
        if item.bought == False: # items that have NOT been bought will be displayed in shop
            priceImg = item.checkPrice(moneyCount.value) # checks if item can be bought based on how much money the user has 
            item.render_img(priceImg) # renders item as a result, normal img if it can be bought or alt img if it is too expensive
            # finds the corresponding button from buttonList so purchase button is rendered at the appropriate position
            itemIndex = weaponList.index(item)
            itemButton = buttonList[itemIndex]
            itemButton.renderButton()
        else: # items that have been bought will not be shown in shop, they will be replaced by a solid colour rectangle
            shop_rect = pygame.Rect(item.x, item.y, 700, 150)
            display.fill('darkslateblue', shop_rect)
    userInventory.render_inventory() 
    backButton.renderButton()
    pygame.display.flip()

# handles purchases by finding which purchase button was clicked and eliciting the appropriate response
def runShop(x,y, buttonList, shopWeaponsList, moneyCount, inventory, weaponsList): 
    for index, button in enumerate(buttonList): 
        if button.rect.collidepoint(x,y): 
            item = shopWeaponsList[index] 
            if not (item.bought) and (moneyCount.value >= item.price): # checks item has not already been bought and is not too expensive to be bought
                # actions to enable purchase occur
                item.bought = True
                pygame.mixer.Sound.play(itemBoughtSound)
                moneyCount.decrementValue(item.price)
                inventory.fill_inventory(weaponsList, index)   
            elif not(item.bought): # purchase unsuccessful
                pygame.mixer.Sound.play(failedPurchaseSound)
