import module_manager
module_manager.review()
import random 
import math
import pygame
import os
import string

width = 500
height = 292

class WorldMap(object):
    def __init__(self, numLevel):
        self.allTiles = pygame.sprite.Group()
        self.finishedLine = pygame.sprite.Group()
        auto = Autogeneration(numLevel)
        auto.generateBaseMap()
        self.load_map = auto.tileList

    #drawPlatforms is a modified method based off of snippets of code in Platform.py file downloaded from the download link provided in the youtuber's description on this page: https://www.youtube.com/watch?v=5q7tmIlXROg
    #dirt.png is downloaded from the download link provided in the youtuber's description on this page: https://www.youtube.com/watch?v=5q7tmIlXROg
    #grass.png is downloaded from the download link provided in the youtuber's description on this page: https://www.youtube.com/watch?v=5q7tmIlXROg
    #flagPole png downloaded from https://www.pngfind.com/download/ioRTRo_mario-flag-mario-flag-pixel-art-hd-png/
    def drawPlatforms(self):
        gameMap = self.load_map
        y = 0
        for layer in gameMap:
            x = 0
            for tile in layer:
                if tile == 1:
                    newPlatform1 = CurrentGround(x*16,y*16, "dirt.png")
                    self.allTiles.add(newPlatform1)
                if tile == 2:
                    newPlatform2 = CurrentGround(x*16,y*16, "grass.png")
                    self.allTiles.add(newPlatform2)
                if tile == 5:
                    newPlatform4 = CurrentGround(x*16,y*16, "flagpole.png")
                    self.finishedLine.add(newPlatform4)
                x += 1
            y += 1

class Autogeneration(pygame.sprite.Sprite):
    def __init__(self, numLevel):
        self.numLevel = numLevel
        self.totalShapes = 7 + numLevel
        self.numRow = 24
        self.numCol = 12 * self.totalShapes
        self.tileList = [[0 for i in range(self.numCol)] for j in range(self.numRow)]
        self.shape1 =[[2,0,0,0,0,0,0,0,0, 0,0,2],
                      [1,2,2,2,2,2,2,2,2,2,2,1],
                      [1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,1,1,1,1,1,1,1,1,1,1,1]]

        self.shape2 = [[0,0,0,0,0,0,0,0,0,0,0],
                       [1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1]]

        self.shape3 = [[0,0,0,0,0,0,0,0,0,2],
                       [2,2,2,2,2,2,2,2,2,1]]

        self.shape4 = [[0,0,0,0,0,2,0,0,0,0,0],
                       [1,2,2,2,2,1,2,2,2,2,1],
                       [0,0,0,1,1,1,1,1,0,0,0],
                       [0,0,0,0,1,1,1,0,0,0,0],
                       [0,0,0,0,1,1,1,0,0,0,0],
                       [0,0,0,0,1,1,1,0,0,0,0],
                       [0,0,0,0,1,1,1,0,0,0,0],
                       [0,0,0,0,1,1,1,0,0,0,0],
                       [0,0,0,0,1,1,1,0,0,0,0]]
                       

        self.shape5 = [[0,0,0,2,2,0,0,0,0,2],
                       [0,0,2,1,1,2,2,2,2,1],
                       [0,2,1,1,1,1,1,1,1,1],
                       [2,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1]]

        self.shapeList = dict()
        self.shapeList[1] = self.shape1
        self.shapeList[2] = self.shape2
        self.shapeList[3] = self.shape3
        self.shapeList[4] = self.shape4
        self.shapeList[5] = self.shape5

        self.upperPlatform = dict()
        self.upperPlatform[1] = [[2,2,2,2]]
        self.upperPlatform[2] = [[2,2,2]]
        self.upperPlatform[3] = [[2,2]]
        self.upperPlatform[4] = [[2,2,2,2,2]]
        
        self.highPlatform = dict()
        self.highPlatform[1] = [[2,0,0,0,0,0,2],
                                 [1,2,2,2,2,2,1]]
        self.highPlatform[2] = [[2,0,0,0,0,0,0],
                                 [1,2,2,2,2,2,2]]
        self.highPlatform[3] = [[0,2,2,2,2,2,2],
                                 [2,1,1,1,1,1,1]]
        self.highPlatform[4] = [[0,0,2,0,2,2,2],
                                 [2,2,1,2,1,1,1]]

    def legalBaseMap(self, numRow, numCol, x, y, success):
        noOverlap = True
        for row in range (y, y + numRow):
            for col in range (x, x + numCol):
                if row < 0 or row > len(self.tileList) or col < 0 or col> len(self.tileList[0]):
                    noOverlap = False
                if self.tileList[row][col] != 0:
                    noOverlap = False
        if noOverlap:
            return True
            
    def generateBaseMap(self):
        sectionsOnMap = self.totalShapes
        success = 0
        successPoints = []
        startPoint = 0
        endPoint = self.numCol //sectionsOnMap
        while success < sectionsOnMap - 1:
            legal = False
            while legal == False:
                randShape = random.randint(1, 5)
                randX = startPoint
                randY = random.randint(12, 13)
                shape = self.shapeList[randShape]
                if self.legalBaseMap(len(shape), len(shape[0]), randX, randY, success):
                    for row in range(len(shape)):
                        for col in range(len(shape[0])):
                            self.tileList[row + randY][col + randX] = shape[row][col]
                            legal = True
            success += 1 
            if success <= 2 or success >= 7:
                self.placeUpperPlatform(randY, randX, len(shape[0]))
            if success >=3 and success < 7:
                self.placeHighPlatform(randY, randX, len(shape[0]), success)
            startPoint = col + randX + random.randint(1, 3)
            if success == sectionsOnMap - 1:
                for i in range(0, -1, -1):
                    if self.tileList[randY - i][randX + len(shape[0]) * 3 //4] == 0:
                        self.tileList[randY - i][randX + len(shape[0]) * 3 //4] = 5
                        pass
    
    def placeUpperPlatform(self, randY, randX, width): 
        randPlatform = self.upperPlatform[random.randint(1, len(self.upperPlatform))]
        posY = randY - 3
        posX = random.randint(randX, randX + width - len(randPlatform))
        for row in range(len(randPlatform)):
            for col in range(len(randPlatform[0])):
                self.tileList[posY + row][posX + col] = randPlatform[row][col]
    
    def placeHighPlatform(self, randY, randX, width, success): 
        randPlatform = self.highPlatform[random.randint(1, len(self.highPlatform))]
        posY = randY - 6
        posX = random.randint(randX, randX + width - len(randPlatform))
        for row in range(len(randPlatform)):
            for col in range(len(randPlatform[0])):
                self.tileList[posY + row][posX + col] = randPlatform[row][col]

#player.png is downloaded from the download link provided in the youtuber's description on this page: https://www.youtube.com/watch?v=5q7tmIlXROg
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('player.png').convert()
        self.width = 9
        self.height = 18
        self.surf = pygame.transform.scale(self.surf, (self.width,self.height))
        self.surf.set_colorkey((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.x = 120
        self.rect.y = 7*16
        self.playerXChange = 0
        self.playerYChange = 0
        self.jumping = False
        self.timer = 14
    
    #code for moving player through keyboard movement is modified from a user named GRC on stackoverflow https://stackoverflow.com/questions/14087609/smooth-keyboard-movement-in-pygame
    def playerKeyboardMove(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.playerXChange = -4
            if event.key == pygame.K_RIGHT:
                self.playerXChange = 4
            if event.key == pygame.K_UP:
                self.jumping = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.playerXChange = 0

# wings png downloaded from https://www.pngfind.com/download/hxhwomJ_wing-angel-angels-wings-angelwings-angelwing-golden-wings/
class Wings(pygame.sprite.Sprite):
    def __init__(self):
        super(Wings, self).__init__()
        self.surf = pygame.image.load('wings.png').convert()
        self.width = 40
        self.height = 30
        self.surf = pygame.transform.scale(self.surf, (self.width,self.height))
        self.rect = self.surf.get_rect()
        self.rect.x = 0
        self.rect.y = 0

#pink egg png: https://www.seekpng.com/ipng/u2q8q8a9a9a9r5e6_pink-yoshi-egg-pink-yoshi-egg-png/
#blue egg png: https://www.pngkit.com/downpic/u2e6y3i1u2a9y3a9_light-blue-yoshi-egg/
#green egg png: https://www.hiclipart.com/free-transparent-background-png-clipart-zjmuo
class Egg(pygame.sprite.Sprite):
    def __init__(self, color):
        super(Egg, self).__init__()
        self.eggColorFile = color + 'Egg.png'
        self.width = 15
        self.height = 15
        self.surf = pygame.image.load(self.eggColorFile).convert()
        self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
        self.surf.set_colorkey((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.x = 150
        self.rect.y = 7*16 
        self.activated = False
        self.eggXChange = 0
        self.eggFrozen = False

#monster png from https://www.freepngimg.com/png/34076-blue-monster-transparent/icon
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.width = 15
        self.height = 20
        self.surf = pygame.image.load("monster.png").convert()
        self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect()
        self.rect.x = 3*16
        self.rect.y = 5*16
        self.falling = True
        self.goRight = True
        self.jumping = False
        self.chasing = False 
        self.timer = 20
        self.jumpTimer = 20

class CurrentGround(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super(CurrentGround, self).__init__()
        self.surf = pygame.image.load(image).convert()
        self.surf.set_colorkey((0,0,0))
        self.width = 16
        self.height = 16
        self.surf = pygame.transform.scale(self.surf, (self.width,self.height))
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y

#find the RGB values of the colors
def commonColors(colorName):
    if colorName == "pastelBlue":
        return (209, 243, 255) 
    elif colorName == "pastelPink":
        return (255, 209, 220)
    elif colorName == "pastelGreen":
        return (220, 255, 209)
    elif colorName == "Green":
        return (0,100,0)

class AllLevels(object):
    def __init__(self, numLevel, totalEggs): 
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Save the Birds!")
        self.margin = 120
        self.numLevel = numLevel
        self.player = Player()
        currentGround = WorldMap(self.numLevel)
        currentGround.drawPlatforms()
        wings = Wings()
        self.allWings = pygame.sprite.Group()
        self.allWings.add(wings)
        self.allCurrentGrounds = currentGround.allTiles 
        self.finishedLine = currentGround.finishedLine
        self.allEnemies = self.enemyRandPos(currentGround.load_map)
        self.allEggs = self.eggRandPos(currentGround.load_map)
        self.allEggs = self.allEggs
        self.allEnemies = self.allEnemies
        self.healthBar = 120
        self.seconds = 30
        self.clock = 50
        if numLevel > 1:
            self.clock += (numLevel-1) * 10
        self.numGetWings = 1
        self.canGetWings = False
        self.wingsTimer = 0
        self.jumpTimer = 14
        self.wingsSeconds = 30
        self.totalEggs = totalEggs
        self.firstWin = 1
        self.numEggStacks = 2

    def enemyRandPos(self, gameMap):
        startingNumEnemy = 2
        allEnemies = pygame.sprite.Group()
        row = len(gameMap)
        col = len(gameMap[0])
        for i in range(startingNumEnemy + self.numLevel): 
            enemy = Enemy()
            hasPlatform = False
            enemy.rect.x = -1
            while (self.player.rect.x >= enemy.rect.x and self.player.rect.x <= enemy.rect.x + 16) or (not hasPlatform):
                hasPlatform = False
                enemy.rect.x = random.randint(self.player.rect.x//16 * 2, col-1)
                for i in range(len(gameMap)):
                    if gameMap[i][enemy.rect.x] != 0:
                        hasPlatform = True
                enemy.rect.x *= 16
            enemy.rect.y = row * 16 //4
            allEnemies.add(enemy)
        return allEnemies

    def eggRandPos(self, gameMap):
        allEggs = pygame.sprite.Group()
        row = len(gameMap) 
        col = len(gameMap[0]) 
        colors = dict()
        colors[0] = "Pink" 
        colors[1] = "Blue" 
        colors[2] = "Pink"
        for i in range(3):
            egg = Egg(colors[i])
            hasPlatform = False
            egg.rect.x = -1
            while (self.player.rect.x >= egg.rect.x and self.player.rect.x <= egg.rect.x + 16) or (not hasPlatform):
                hasPlatform = False
                egg.rect.x = random.randint(0, col*2//3)
                for i in range(len(gameMap)):
                    if gameMap[i][egg.rect.x] != 0:
                        hasPlatform = True
                egg.rect.x *= 16
            egg.rect.y = row * 16 //3
            allEggs.add(egg)
        return allEggs

    def collision(self,player):
        (collision, bottomCollision, tileY) = (False, False, 0)
        for tile in self.allCurrentGrounds:
            if pygame.sprite.collide_rect(player, tile):
                if player.rect.y + player.height >= tile.rect.y and player.rect.y + player.height <= tile.rect.y + tile.height:
                    if player.rect.x > tile.rect.x and player.rect.x < tile.rect.x + tile.width:
                        (colllision, bottomCollision, tileY) = (True, True, tile.rect.y) 
                    elif player.rect.x + player.width > tile.rect.x and player.rect.x + player.width < tile.rect.x + tile.width:
                        (colllision, bottomCollision, tileY) = (True, True, tile.rect.y) 
                collision = True
        return (collision, bottomCollision, tileY)

    def playerMove(self):
        self.player.rect.x += self.player.playerXChange
        (collision, bottomCollision, tileY) = self.collision(self.player)
        for egg in self.allEggs:
            if egg.eggFrozen:
                if pygame.sprite.collide_rect(self.player, egg):
                    self.player.rect.x -= self.player.playerXChange
        if self.player.rect.x+5 > width or self.player.rect.x < 0 or collision:
            self.player.rect.x -= self.player.playerXChange
        if self.player.jumping:  
            if self.player.timer > self.jumpTimer//2:
                self.player.rect.y -= 9
                (collision, bottomCollision, tileY) = self.collision(self.player)
                if collision == True and bottomCollision == False:
                    self.player.rect.y += 9
                if collision == True and bottomCollision == True:
                    self.player.rect.y = tileY - self.player.height
                    self.player.jumping = False
                    self.player.timer = self.jumpTimer
                for egg in self.allEggs:
                    if egg.eggFrozen:
                        (collision, bottomCollision, tileY) = self.eggCollision(self.player, egg)
                        if collision == True and bottomCollision == False:
                            self.player.rect.y += 9
                        if collision == True and bottomCollision == True:
                            self.player.rect.y = tileY - self.player.height
                            self.player.jumping = False
                            self.player.timer = self.jumpTimer
            else:
                self.player.rect.y += 9
                (collision, bottomCollision, tileY) = self.collision(self.player)
                if collision == True and bottomCollision == False:
                    self.player.rect.y -= 9
                if collision == True and bottomCollision == True:
                    self.player.rect.y = tileY - self.player.height
                    self.player.jumping = False
                    self.player.timer = self.jumpTimer
                for egg in self.allEggs:
                    if egg.eggFrozen:
                        if pygame.sprite.collide_rect(self.player, egg):
                            self.player.rect.y = egg.rect.y - self.player.height
                            self.player.jumping = False
                            self.player.timer = self.jumpTimer
                            pass
            self.player.timer -= 1
            if self.player.timer == 0 and not self.canGetWings:
                self.player.jumping = False
                self.player.timer = self.jumpTimer
        else:
            self.player.rect.y +=5
            (collision, bottomCollision, tileY) = self.collision(self.player)
            if bottomCollision:
                self.player.rect.y = tileY - self.player.height
            for egg in self.allEggs:
                if egg.eggFrozen:
                    if pygame.sprite.collide_rect(self.player, egg):
                                    self.player.rect.y = egg.rect.y - self.player.height  
                
    def eggCollision(self, player, egg):
        (collision, bottomCollision, tileY) = (False, False, 0)
        if pygame.sprite.collide_rect(player, egg):
            if player.rect.y + player.height >= egg.rect.y and player.rect.y + player.height <= egg.rect.y + egg.height:
                if player.rect.x > egg.rect.x and player.rect.x < egg.rect.x + egg.width:
                    (colllision, bottomCollision, tileY) = (True, True, egg.rect.y) 
                elif player.rect.x + player.width > egg.rect.x and player.rect.x + player.width < egg.rect.x + egg.width:
                    (colllision, bottomCollision, tileY) = (True, True, egg.rect.y) 
            collision = True
        return ((collision, bottomCollision, tileY))

    def eggMove(self):
        for egg in self.allEggs:
            if not egg.eggFrozen:
                if pygame.sprite.collide_rect(egg, self.player):
                    egg.activated = True
                if egg.activated:
                    egg.rect.x += self.player.playerXChange 
                    (collision, bottomCollision, tileY) = self.collision(egg)
                    if egg.rect.x+5 > width or egg.rect.x < 0 or collision:
                        egg.rect.x -= self.player.playerXChange
                if self.player.jumping and egg.activated:    
                    if self.player.timer + 1> self.jumpTimer//2:
                        egg.rect.y -= 9
                        (collision, bottomCollision, tileY) = self.collision(egg)
                        if collision == True and bottomCollision == False:
                            egg.rect.y += 9
                        if collision == True and bottomCollision == True:
                            egg.rect.y = tileY - egg.height
                    else:
                        egg.rect.y += 9
                        (collision, bottomCollision, tileY) = self.collision(egg)
                        if collision == True and bottomCollision == False:
                            egg.rect.y -= 9
                        if collision == True and bottomCollision == True:
                            egg.rect.y = tileY - egg.height
                else:
                    egg.rect.y += 5 
                    (collision, bottomCollision, tileY) = self.collision(egg)
                    if bottomCollision:
                        egg.rect.y = tileY - egg.height

    def getWings(self):
        if self.numGetWings > 0:
            for egg in self.allEggs:
                if egg.activated:
                    self.canGetWings = True
                    pass     
        if self.canGetWings:
            self.numGetWings -= 1
            for wing in self.allWings:
                wings = Wings()
                wings.surf = pygame.transform.scale(wings.surf, (20,20))
                self.screen.blit(wings.surf, (2, 54))
                #codes for the font and text is modified from https://pygame.readthedocs.io/en/latest/4_text/text.html
                font1 = pygame.font.SysFont('chalkduster.ttf', 11)
                img = font1.render('Press Space Bar', True, (0,0,0))
                self.screen.blit(img, (24,54))
                font2 = pygame.font.SysFont('chalkduster.ttf', 11)
                img = font2.render('to use Power Up', True, (0,0,0))
                self.screen.blit(img, (24,64))
        if self.wingsTimer > 0:
            self.jumpTimer = 22
            self.wingsSeconds -= 1
            if self.wingsSeconds < 0:
                self.wingsTimer -= 1
                self.wingsSeconds = 30
            #codes for the font and text is modified from https://pygame.readthedocs.io/en/latest/4_text/text.html
            font1 = pygame.font.SysFont('chalkduster.ttf', 10)
            img = font1.render('Power Up Timer' + str(self.wingsTimer), True, (0,0,0))
            self.screen.blit(img, (15,50))
            wing = Wings()
            wing.surf.set_colorkey((0,0,0))
            self.screen.blit(wing.surf, (self.player.rect.x - wing.width//2, self.player.rect.y - wing.height))
        else:
            self.jumpTimer = 14

    def enemyMoveDir(self):
        for enemy in self.allEnemies:
            if not enemy.chasing or abs(enemy.rect.x - self.player.rect.x) >= 60:
                self.enemyMove(enemy)
            if abs(enemy.rect.x - self.player.rect.x) <= 60:
                enemy.chasing = True
                self.enemyChasePlayer(enemy)
            if self.numLevel > 1:
                if self.seconds <= 1:
                    enemy.jumping = True
                if enemy.jumping:  
                    if enemy.timer > enemy.jumpTimer//2:
                        enemy.rect.y -= 4
                        (collision, bottomCollision, tileY) = self.collision(enemy)
                        if collision == True and bottomCollision == False:
                            enemy.rect.y += 4
                        if collision == True and bottomCollision == True:
                            enemy.rect.y = tileY - enemy.height
                            enemy.jumping = False
                            enemy.timer = enemy.jumpTimer
                    else:
                        enemy.rect.y += 4
                        (collision, bottomCollision, tileY) = self.collision(enemy)
                        if collision == True and bottomCollision == False:
                            enemy.rect.y -= 4
                        if collision == True and bottomCollision == True:
                            enemy.rect.y = tileY - enemy.height
                            enemy.jumping = False
                            enemy.timer = enemy.jumpTimer
                    enemy.timer -= 1

    def enemyCollision(self):
        for enemy in self.allEnemies:
            if pygame.sprite.collide_rect(self.player, enemy):
                self.healthBar -= 5
                return True

    def enemyDetectBottomCollision(self, enemy, movingSpeed, fallingSpeed):
        enemy.rect.y += fallingSpeed
        (collision, bottomCollision, tileY) = self.collision(enemy)
        if not bottomCollision and not enemy.jumping:
            enemy.goRight = not enemy.goRight
            enemy.rect.x -= movingSpeed
        enemy.rect.y -= fallingSpeed

    def enemyChasePlayer(self, enemy):
        fallingSpeed = 5
        movingSpeed = 3
        if enemy.rect.x < self.player.rect.x:
            enemy.rect.x += movingSpeed
            (collision, bottomCollision, tileY) = self.collision(enemy)
            if self.enemyCollision() or collision:
                enemy.goRight = not enemy.goRight
                enemy.rect.x -= movingSpeed
            else: 
                self.enemyDetectBottomCollision(enemy, movingSpeed, fallingSpeed)
        elif enemy.rect.x > self.player.rect.x:
            enemy.rect.x -= movingSpeed
            (collision, bottomCollision, tileY) = self.collision(enemy)
            if self.enemyCollision() or collision:
                enemy.rect.x += movingSpeed
                enemy.goRight = not enemy.goRight
                enemy.chasing = False
            else:
                self.enemyDetectBottomCollision(enemy, -1 * movingSpeed, fallingSpeed)
            
    def enemyMove(self, enemy):
        fallingSpeed = 5
        movingSpeed = 2
        if enemy.falling:
            enemy.rect.y += fallingSpeed
            (collision, bottomCollision, tileY) = self.collision(enemy)
            if bottomCollision:
                enemy.rect.y =  tileY - enemy.height
                enemy.falling = False
        else:
            if enemy.goRight:
                enemy.rect.x += movingSpeed
                (collision, bottomCollision, tileY) = self.collision(enemy)
                if collision:
                    enemy.rect.x -= movingSpeed
                    enemy.goRight = False
                else:
                    self.enemyDetectBottomCollision(enemy, movingSpeed, fallingSpeed)
            else:
                enemy.rect.x -= movingSpeed
                (collision, bottomCollision, tileY) = self.collision(enemy)
                if collision:
                    enemy.rect.x += movingSpeed
                    enemy.goRight = True
                else:
                    self.enemyDetectBottomCollision(enemy, -1 * movingSpeed, fallingSpeed)
            
    def draw(self):
        if self.player.rect.x < self.margin or self.player.rect.x > width - self.margin: 
            self.player.rect.x -= self.player.playerXChange
            for egg in self.allEggs:
                egg.rect.x -= self.player.playerXChange
            for enemy in self.allEnemies:
                enemy.rect.x -= self.player.playerXChange
            for currentGround in self.allCurrentGrounds:
                currentGround.rect.x -= self.player.playerXChange
            for tile in self.finishedLine:
                tile.rect.x -= self.player.playerXChange
    
    def eggGather(self):
        for egg in self.allEggs:
            if egg.activated:
                if self.player.rect.x > egg.rect.x:
                    egg.rect.x += egg.eggXChange
                else:
                    egg.rect.x -= egg.eggXChange
    
    def eggStackRight(self):
        if self.numEggStacks > 0:
            i = 0
            for egg in self.allEggs:
                if egg.activated:
                    egg.rect.x = self.player.rect.x + self.player.width + i * egg.width 
                    egg.rect.y = self.player.rect.y - i * egg.height 
                    egg.eggFrozen = True
                    i += 1
            self.numEggStacks -= 1

    def winning(self):
        numEggs = 0
        win = False
        eggIntact = False
        for tile in self.finishedLine:
            if pygame.sprite.collide_rect(self.player, tile) or self.player.rect.x > tile.rect.x:
                win = True
        if win:
            for egg in self.allEggs:
                if egg.activated and abs(egg.rect.x - self.player.rect.x) < egg.width + self.player.width:
                    numEggs += 1
            if self.firstWin == 1:
                self.totalEggs += numEggs
                self.firstWin -= 1
            if self.numLevel == 3:
                newSurf = pygame.Surface((width, height))
                newSurf.fill((209, 243, 255))
                self.screen.blit(newSurf, (0,0))
                #codes for the font and text is modified from https://pygame.readthedocs.io/en/latest/4_text/text.html
                font4 = pygame.font.SysFont('chalkduster.ttf', 18)
                img3 = font4.render("You have completed all the levels!", True, (0,0,0))
                font5 = pygame.font.SysFont('chalkduster.ttf', 15)
                img4 = font5.render('Click x on the window to exit!', True, (0,0,0))
                self.screen.blit(img3, (width//6, height//4))
                self.screen.blit(img4, (width//5, height//3))
                font6 = pygame.font.SysFont('chalkduster.ttf', 15)
                img5 = font6.render('Total Eggs Accumulated: ' + str(self.totalEggs), True, (0,0,0))
                self.screen.blit(img5, (width//5, height//2))
            else:
                #codes for the font and text is modified from https://pygame.readthedocs.io/en/latest/4_text/text.html
                font1 = pygame.font.SysFont('chalkduster.ttf', 30)
                img = font1.render('You Win!!', True, (0,0,0))
                font2 = pygame.font.SysFont('chalkduster.ttf', 15)
                img1 = font2.render('Press down arrow key to advance to the next level.', True, (0,0,0))
                font3 = pygame.font.SysFont('chalkduster.ttf', 20)
                img2 = font3.render("You have brought back " + str(numEggs) + " eggs!", True, (0,0,0))
                newSurf = pygame.Surface((width, height))
                newSurf.fill((209, 243, 255))
                self.screen.blit(newSurf, (0, 0))
                self.screen.blit(img, (width//4, height//4))
                self.screen.blit(img1, (width//12, height//2))
                self.screen.blit(img2, (width//8, height* 3//4))
                font4 = pygame.font.SysFont('chalkduster.ttf', 15)
                img3 = font4.render('Total Eggs Accumulated: ' + str(self.totalEggs), True, (0,0,0))
                self.screen.blit(img3, (width//5, height//2 + 20))
            return ((True, numEggs))
        return ((False, numEggs))
            
    #codes for the font and text is modified from https://pygame.readthedocs.io/en/latest/4_text/text.html
    def losing(self):
        font1 = pygame.font.SysFont('chalkduster.ttf', 30)
        img = font1.render('Game Over!!', True, (0,0,0))
        font2 = pygame.font.SysFont('chalkduster.ttf', 15)
        img1 = font2.render('Press down arrow key to play again.', True, (0,0,0))
        if self.player.rect.y > height or self.healthBar <= 0 or self.clock <= 0:
            newSurf = pygame.Surface((width, height))
            newSurf.fill((209, 243, 255))
            self.screen.blit(newSurf, (0, 0))
            self.screen.blit(img, (width//4, height//4))
            self.screen.blit(img1, (width//8, height//2))
            return True

    def settingUpBackground(self):
        #background.png downloaded from https://opengameart.org/content/country-side-platform-tiles
        surf = pygame.image.load('background.png').convert()
        self.screen.blit(surf, (0, 0))
        for currentGround in self.allCurrentGrounds:
            self.screen.blit(currentGround.surf, (currentGround.rect.x, currentGround.rect.y))
        titleSurf = pygame.Surface((width//5 + 5, 42))
        titleSurf.fill((146,183,254))
        self.screen.blit(titleSurf, (0,0))
        #codes for the font and text is modified from https://pygame.readthedocs.io/en/latest/4_text/text.html
        font1 = pygame.font.SysFont('chalkduster.ttf', 10)
        img = font1.render('Collect Eggs by touching the eggs!', True, (0,0,0))
        self.screen.blit(img, (width//3, 10))
        self.seconds -= 1
        if self.seconds == 0:
            self.clock -= 1
            self.seconds = 30
        font2 = pygame.font.SysFont('freesansbold.ttf', 10)
        img1 = font1.render('Timer: ' + str(self.clock), True, (0,0,0))
        self.screen.blit(img1, (20, 40))
        font3 = pygame.font.SysFont('chalkduster.ttf', 10)
        img = font1.render('Health Bar', True, (0,0,0))
        self.screen.blit(img, (15, 10))

    def checkEggs(self, event):
        for egg in self.allEggs:
            if egg.activated:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        egg.eggXChange = 3
                    if event.key == pygame.K_f:
                        self.eggStackRight()
                elif event.type == pygame.KEYUP:
                    egg.eggXChange  = 0
                pressed = pygame.key.get_pressed()
                if not pressed[pygame.K_f]:
                    if egg.eggFrozen:
                        egg.eggFrozen = False
    
    def checkAbility(self):
        hasAbility = False
        for egg in self.allEggs:
            if self.numEggStacks > 0 and egg.activated:
                hasAbility = True
        if hasAbility:
            surf = pygame.Surface((12,12))
            surf.fill(commonColors('pastelPink'))
            self.screen.blit(surf, (2, 80))
            font1 = pygame.font.SysFont('chalkduster.ttf', 10)
            img = font1.render(str(self.numEggStacks) + " tries of stacking egg abililty left", True, (0,0,0))
            self.screen.blit(img, (24, 80))
            font2 = pygame.font.SysFont('chalkduster.ttf', 10)
            img1 = font2.render("(press f to activate)", True, (0,0,0))
            self.screen.blit(img1, (26, 90))

    def run(self):
        pygame.init()
        running = True
        while running:
            self.settingUpBackground()
            self.getWings()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        return True
                self.checkEggs(event)
                self.player.playerKeyboardMove(event)
                if self.canGetWings:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.canGetWings = False
                            self.wingsTimer = 3
                if self.losing():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            return False
                (won, numEggs) = self.winning()
                if won:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            return True
                        elif event.key == pygame.K_UP:
                            return True  
            self.playerMove()
            self.eggGather()
            self.eggMove()
            self.enemyMoveDir()
            self.draw()
            self.screen.blit(self.player.surf, (self.player.rect.x, self.player.rect.y))
            for enemy in self.allEnemies:
                self.screen.blit(enemy.surf, (enemy.rect.x, enemy.rect.y))
            for egg in self.allEggs:
                self.screen.blit(egg.surf, (egg.rect.x, egg.rect.y))
            for finishedLine in self.finishedLine:
                self.screen.blit(finishedLine.surf, (finishedLine.rect.x, finishedLine.rect.y))
            self.checkAbility()
            #codes for the font and text is modified from https://pygame.readthedocs.io/en/latest/4_text/text.html
            font10 = pygame.font.SysFont('chalkduster.ttf', 15)
            img10 = font10.render("Level " + str(self.numLevel), True, (0,0,0))
            self.screen.blit(img10, (width//2 - 20, 30))
            if not self.losing():
                healthBarSurf = pygame.Surface((122,15))
                self.screen.blit(healthBarSurf, (15, 25))
                healthProgress = pygame.Surface((self.healthBar,13))
                healthProgress.fill((255,255,255))
                self.screen.blit(healthProgress, (16,26))
            self.winning()
            pygame.display.flip()
        return None

def runLoop():
    numTries = 0
    totalEggs = 0
    i = 1
    running = False
    while not running:
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        #background.png downloaded from https://opengameart.org/content/country-side-platform-tiles
        surf = pygame.image.load('background.png').convert()
        screen.blit(surf, (0,0))
        titleSurf = pygame.Surface((width//5 + 5, 42))
        titleSurf.fill((146,183,254))
        screen.blit(titleSurf, (0,0))
        #codes for the font and text is modified from https://pygame.readthedocs.io/en/latest/4_text/text.html
        font1 = pygame.font.SysFont('chalkduster.ttf', 25)
        img = font1.render('Catch the Hatchlings!!', True, (0,0,0))
        screen.blit(img, (width//5, height//5))
        font2 = pygame.font.SysFont('chalkduster.ttf', 12)
        img1 = font2.render('Press down arrow button to play', True, (0,0,0))
        font3 = pygame.font.SysFont('chalkduster.ttf', 10)
        screen.blit(img1, (width//5 + 20, height//3))
        img2 = font3.render('Keyboard: r = collecting eggs, f = egg stack, space bar for wings power up', True, (0,0,0))
        screen.blit(img2, (15, 120))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    font1 = pygame.font.SysFont('chalkduster.ttf', 10)
                    img = font1.render('Please wait...', True, (0,0,0))
                    screen.blit(img, (width//3, height//2))
                    pygame.display.flip()
                    running = True
        pygame.display.flip()
    while running and i < 4:
        playGame = AllLevels(i, totalEggs)
        result = playGame.run()
        if result == None:
            pygame.quit()
            os._exit(0)
            running = False
        while running and result != True:
            if result == None:
                pygame.quit()
                os._exit(0)
                running = False
            else:
                playGame = AllLevels(i, totalEggs)
                result = playGame.run()
        totalEggs = playGame.totalEggs
        i += 1

runLoop()


