#Filename spaceattackV120.py
#Author: Trevor Hebert
#Last Modified by: Trevor Hebert
#Date Last Modified: August 7, 2012
#Program Description: This is a simple space invaders type game where you avoid the obstacles while shooting things for points.
#Revision History: 1.2.0
#                  1.1.0
#                  1.0.0
#   Recently added
# - Added Alien enemy
# - Added more accurate game difficulties
# - update GUI


import pygame, gameEngine, random, sys

#ship class
class Ship(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("ship.gif")
        self.setSpeed(0)
        self.setAngle(0)
        self.bulletcounter = 1
        
        #check for key presses
    def checkEvents(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rotateBy(5)
        if keys[pygame.K_RIGHT]:
            self.rotateBy(-5)
        if keys[pygame.K_UP]:
            self.addForce(.2, self.rotation)
            self.setImage("shipthrust.gif")
        if not keys[pygame.K_UP]:
            self.setImage("ship.gif")
        if keys[pygame.K_DOWN]:
            self.addForce(-.2, self.rotation)
        if keys[pygame.K_SPACE]:
            if self.bulletcounter == 1:
                self.scene.bullet.fire()
            elif self.bulletcounter == 2:
                self.scene.bullet2.fire()
            elif self.bulletcounter == 3:
                self.scene.bullet3.fire()
            elif self.bulletcounter == 4:
                self.scene.bullet4.fire()
            elif self.bulletcounter == 5:
                self.scene.bullet5.fire()
                self.bulletcounter = 0    
            self.bulletcounter += 1
            
         
    
#bullet class    
class Bullet(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("bullet.gif")
        self.imageMaster = pygame.transform.scale(self.imageMaster, (5, 5))
        self.setBoundAction(self.HIDE)
        self.reset()
        
    def fire(self):
        self.setPosition((self.scene.ship.x, self.scene.ship.y))
        self.setSpeed(15)
        self.setAngle(self.scene.ship.rotation)
        
    def reset(self):
        self.setPosition ((-100, -100))
        self.setSpeed(0)
        
#rock class    
class Rock(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("asteroid.gif")
        self.reset()
        
    def checkEvents(self):
        self.rotateBy(self.rotSpeed)
        
    def reset(self):
        """ change attributes randomly """
        
        #set random position
        x = random.randint(0, self.screen.get_width())
        y = random.randint(0, self.screen.get_height())
        self.setPosition((x, y))
        
        #set random size
        scale = random.randint(10, 40)
        self.setImage("asteroid.gif")
        self.imageMaster = \
            pygame.transform.scale(self.imageMaster, (scale, scale))
        
        self.setSpeed(random.randint(0, 6))
        self.setAngle(random.randint(0, 360))
        self.rotSpeed = random.randint(-5, 5)

#blackhole class
class Blackhole(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("blackhole.gif")
        self.reset()
        
    def checkEvents(self):
        self.rotateBy(self.rotSpeed)
        
    def reset(self):
        """ change attributes randomly """
        
        #set random position
        x = random.randint(0, self.screen.get_width())
        y = random.randint(0, self.screen.get_height())
        self.setPosition((x, y))
        
        #set random size
        scale = random.randint(10, 40)
        self.setImage("blackhole.gif")
        self.imageMaster = \
            pygame.transform.scale(self.imageMaster, (scale, scale))
        
        self.setSpeed(random.randint(0, 6))
        self.setAngle(random.randint(0, 360))
        self.rotSpeed = random.randint(-5, 5)

#alien class
class Alien(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("enemyship.gif")
        self.reset()
        
    def checkEvents(self):
        self.rotateBy(self.rotSpeed)
        
    def reset(self):
        """ change attributes randomly """
        
        #set random position
        x = random.randint(0, self.screen.get_width())
        y = random.randint(0, self.screen.get_height())
        self.setPosition((x, y))
        
        #set random size
        scale = random.randint(10, 40)
        self.setImage("enemyship.gif")
        self.imageMaster = \
            pygame.transform.scale(self.imageMaster, (scale, scale))
        
        self.setSpeed(random.randint(4, 9))
        self.setAngle(random.randint(0, 360))
        self.rotSpeed = random.randint(-5, 0)

#healthbar class
class HealthBar(gameEngine.SuperSprite):
    def __init__(self, scene, playerHealth):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("health5.gif")
        #self.reset()
        self.setPosition((560,20))
        self.initialHealth = playerHealth
        self.health = self.initialHealth
    
    def decrementHealth(self, amount):  #decrements health by the amount given and calls the update
        self.health -= amount
        if self.health <= 0:
            self.health = self.initialHealth
        self.updateHealth()
    
    def updateHealth(self): #updates the healthbar image
        if self.health == 5:
            self.setImage("health5.gif")
        if self.health == 4:
            self.setImage("health4.gif")
        if self.health == 3:
            self.setImage("health3.gif")
        if self.health == 2:
            self.setImage("health2.gif")
        if self.health == 1:
            self.setImage("health1.gif")
    
    def reset(self):    #resets the healthbar to full
        self.setImage("health5.gif")    
    
         
#game class        
class Game(gameEngine.Scene):
    def __init__(self, difficulty):
        gameEngine.Scene.__init__(self)
        self.ship = Ship(self)  #create the ship
        self.bullet = Bullet(self)  #create bullet 1
        self.bullet2 = Bullet(self)  #create bullet 2
        self.bullet3 = Bullet(self)  #create bullet 3
        self.bullet4 = Bullet(self)  #create bullet 4
        self.bullet5 = Bullet(self)  #create bullet 5
        
        
        self.blackhole = Blackhole(self)    #create blackhole
        self.alien = Alien(self)    #create alien
        self.scoreboard = gameEngine.Label()    #create scoreboard
        self.scoreboard.center = (100, 20)  #place it top left
        self.scoreboard.size = (250,30) 
        self.scoreboard.bgColor = (0x00, 0x00, 0x00)
        self.scoreboard.fgColor = (0x00, 0xCC, 0x00)
        
        self.blackholefix = 0   #counter to fix blackhole colliding with ship automatically
        self.rockfix = 0        #counter to fix rock colliding with ship automatically
        self.alienfix = 0       #counter to fix alien colliding with ship automatically
        self.difficulty = difficulty #game get game difficulty
        
        #set number of enemies for each difficulty
        self.easynumberblackholes = 1
        self.easynumberrocks = 5
        self.easynumberaliens = 3
        self.mediumnumberblackholes = 2
        self.mediumnumberrocks = 8
        self.mediumnumberaliens = 5
        self.hardnumberblackholes = 3
        self.hardnumberrocks = 10
        self.hardnumberaliens = 7
        
        
        
        self.score = -3000  #player score with fixed offset
        self.health = 5 #player health
        self.lives = 3 #player lives
        self.healthBar = HealthBar(self, self.health)
        
        #create list of rocks, aliens and blackholes depending on game difficulty
        self.rocks = []
        self.aliens = []
        self.blackholes = []
        if self.difficulty == "Easy":
            for i in range(self.easynumberrocks): #make easy number rocks
                self.rocks.append(Rock(self))
            for i in range(self.easynumberaliens): #make easy number aliens
                self.aliens.append(Alien(self)) 
            for i in range(self.easynumberblackholes): #make easy number of blackholes
                self.blackholes.append(Blackhole(self))    
        elif self.difficulty == "Medium":
            for i in range(self.mediumnumberrocks): #make medium number rocks
                self.rocks.append(Rock(self))
            for i in range(self.mediumnumberaliens): #make medium number aliens
                self.aliens.append(Alien(self))
            for i in range(self.mediumnumberblackholes): #make medium number blackholes
                self.blackholes.append(Blackhole(self))
        elif self.difficulty == "Hard":
            for i in range(self.hardnumberrocks): #make medium number rocks
                self.rocks.append(Rock(self))
            for i in range(self.mediumnumberrocks): #make medium number rocks
                self.rocks.append(Rock(self))
            for i in range(self.mediumnumberrocks): #make medium number rocks
                self.rocks.append(Rock(self))
                 
             
        self.alienGroup = self.makeSpriteGroup(self.aliens) 
        self.rockGroup = self.makeSpriteGroup(self.rocks)
        self.blackholeGroup = self.makeSpriteGroup(self.blackholes)
        self.addGroup(self.rockGroup)
        self.addGroup(self.blackholeGroup)
        self.addGroup(self.alienGroup)
        
        self.sprites = [self.bullet, self.bullet2, self.bullet3, self.bullet4, self.bullet5, self.ship, self.scoreboard, self.healthBar]
        self.setCaption("Space Attack")       
        
        
    def update(self):
        self.updateScore()
        
        # if rock hits ship
        rockHitShip = self.ship.collidesGroup(self.rocks)
        if rockHitShip:
            if self.rockfix > 0:
                rockHitShip.reset()
                self.health -= 1
                self.healthBar.decrementHealth(1)
            self.rockfix += 1
        
        #if bullet hits a rock
        rockHitBullet = self.bullet.collidesGroup(self.rocks)
        rockHitBullet2 = self.bullet2.collidesGroup(self.rocks)
        rockHitBullet3 = self.bullet3.collidesGroup(self.rocks)
        rockHitBullet4 = self.bullet4.collidesGroup(self.rocks)
        rockHitBullet5 = self.bullet5.collidesGroup(self.rocks)
        if rockHitBullet:
            rockHitBullet.reset()
            self.bullet.reset()
            self.score += 100
        if rockHitBullet2:
            rockHitBullet2.reset()
            self.bullet2.reset()
            self.score += 100
        if rockHitBullet3:
            rockHitBullet3.reset()
            self.bullet3.reset()
            self.score += 100
        if rockHitBullet4:
            rockHitBullet4.reset()
            self.bullet4.reset()
            self.score += 100
        if rockHitBullet5:
            rockHitBullet5.reset()
            self.bullet5.reset()
            self.score += 100
            
        #if bullet hits a rock
        alienHitBullet = self.bullet.collidesGroup(self.aliens)
        alienHitBullet2 = self.bullet2.collidesGroup(self.aliens)
        alienHitBullet3 = self.bullet3.collidesGroup(self.aliens)
        alienHitBullet4 = self.bullet4.collidesGroup(self.aliens)
        alienHitBullet5 = self.bullet5.collidesGroup(self.aliens)
        if alienHitBullet:
            alienHitBullet.reset()
            self.bullet.reset()
            self.score += 500
        if alienHitBullet2:
            alienHitBullet2.reset()
            self.bullet2.reset()
            self.score += 500
        if alienHitBullet:
            alienHitBullet.reset()
            self.bullet3.reset()
            self.score += 500
        if alienHitBullet4:
            alienHitBullet4.reset()
            self.bullet4.reset()
            self.score += 500
        if alienHitBullet5:
            alienHitBullet5.reset()
            self.bullet5.reset()
            self.score += 500    
            
            
        #if a blackhole hits the ship    
        blackholeHitShip = self.ship.collidesGroup(self.blackholes)
        
        if blackholeHitShip:
            if self.blackholefix > 0:
                blackholeHitShip.reset()
                self.health -= 1   
                self.healthBar.decrementHealth(1)
            self.blackholefix += 1   
            
        #if a blackhole hits the ship    
        alienHitShip = self.ship.collidesGroup(self.aliens)
        
        if alienHitShip:
            if self.alienfix > 0:
                alienHitShip.reset()
                self.health -= 1   
                self.healthBar.decrementHealth(1)
            self.alienfix += 1   
     
        if self.health <= 0:    #if player ship dead 
            self.lives -= 1 #take away a life
            self.health = 5 # reset health
            self.healthBar.reset() #reset health bar
            
        if self.lives <= 0: #if players have no more lives
            self.stop()
            
            #self.clear()
            #endGui = Gui()
            #endGui.start()
            
            
     
    def updateScore(self):
        score = "Score: %.0f Lives: %.0f" % (self.score, self.lives)
        self.scoreboard.text = score   
    def getScore(self):
        return self.score



class Gui(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self)
        #initialize background to black
        
        self.background.fill((0x00, 0x00, 0x00))
        self.setCaption("Space Attack!") 
        self.addLabels()
        
        self.addButtons()
        self.highScore = 100
        self.sprites = [self.title, self.highscorelabel, self.scorelabel, self.difficultylabel, self.instructions, self.playagain, self.easyButton, self.mediumButton, self.hardButton, self.quitButton]
        
        
    def addLabels(self):    #create title label and set attributes
        self.title = gameEngine.Label()
        self.title.font = pygame.font.Font("goodfoot.ttf", 50)
        self.title.text = "Space Attack!"
        self.title.fgColor = (0x00, 0xCC, 0x00) #white
        self.title.bgColor = (0x00, 0x00, 0x00) #black
        self.title.center = (320, 40)   # top middle
        self.title.size = (250, 50)
    
        self.highscorelabel = gameEngine.Label()
        self.highscorelabel.font = pygame.font.Font("goodfoot.ttf", 40)
        self.highscorelabel.text = "High Score"
        self.highscorelabel.fgColor = (0xCC, 0xCC, 0xCC) #white
        self.highscorelabel.bgColor = (0x00, 0x00, 0x00) #black
        self.highscorelabel.center = (260, 110) # topleft
        self.highscorelabel.size = (180, 50)
    
        self.scorelabel = gameEngine.Label()
        self.scorelabel.font = pygame.font.Font("goodfoot.ttf", 40)
        self.scorelabel.text = "0"
        self.scorelabel.fgColor = (0x00, 0xCC, 0x00) #white
        self.scorelabel.bgColor = (0x00, 0x00, 0x00) #black
        self.scorelabel.center = (415, 110) # topright
        self.scorelabel.size = (150, 50)
        
        self.difficultylabel = gameEngine.Label()
        self.difficultylabel.font = pygame.font.Font("goodfoot.ttf", 40)
        self.difficultylabel.text = "Select Difficulty"
        self.difficultylabel.fgColor = (0xCC, 0xCC, 0xCC) #white
        self.difficultylabel.bgColor = (0x00, 0x00, 0x00) #black
        self.difficultylabel.center = (130, 220) # topright
        self.difficultylabel.size = (250, 50)

        self.playagain = gameEngine.MultiLabel()
        self.playagain.font = pygame.font.Font("goodfoot.ttf", 40)
        self.playagain.textLines = ["You DIED! ", "Play Again?"]
        self.playagain.fgColor = (0x00, 0x00, 0x00) #black
        self.playagain.bgColor = (0x00, 0x00, 0x00) #black
        self.playagain.center = (540, 240)   # top middle
        self.playagain.size = (250, 90)
        
        self.instructions = gameEngine.MultiLabel()
        self.instructions.font = pygame.font.Font("goodfoot.ttf", 30)
        self.instructions.textLines = ["Use the arrows to, "," move and space to fire!"]
        self.instructions.fgColor = (0x00, 0xCC, 0x00) #green
        self.instructions.bgColor = (0x00, 0x00, 0x00) #black
        self.instructions.center = (130, 315)   # top middle
        self.instructions.size = (550, 90)
        
    def addButtons(self):   #add the GUI buttons
        self.easyButton = gameEngine.Button()
        self.easyButton.center = (350, 200)
        self.easyButton.text = "Easy"   #easy button
        self.easyButton.bgColor = (0x00, 0xCC, 0x00) #green
        
        self.mediumButton = gameEngine.Button()
        self.mediumButton.center = (350, 240)
        self.mediumButton.text = "Medium"   #medium button
        self.mediumButton.bgColor = (0xFF, 0xA5, 0x00) #orange
        
        self.hardButton = gameEngine.Button()
        self.hardButton.center = (350, 280)
        self.hardButton.text = "Hard"   #hard button
        self.hardButton.bgColor = (0xCC, 0x00, 0x00) #green
        
        self.quitButton = gameEngine.Button()
        self.quitButton.center = (350, 420)
        self.quitButton.text = "Quit Game"  #quit button
        self.quitButton.bgColor = (0xCC, 0xCC, 0xCC) #white
        
    def update(self):        
        if self.easyButton.clicked: #if easy button was clicked
            game = Game("Easy")
            game.start()
            self.bgReset()
            
        if self.mediumButton.clicked: #if medium button was clicked
            game = Game("Medium")
            game.start()
            self.bgReset()
            
        if self.hardButton.clicked: #if hard button was clicked
            game = Game("Hard")
            game.start()   
            self.bgReset()
            self.playagain.fgColor = (0xCC, 0x00, 0x00) # change color to show play again 
                
            gameScore = game.getScore()
            if gameScore > self.highScore:
                self.highScore = gameScore
            scoreString = self.highScore.__str__()
            self.scorelabel.text = scoreString
        elif self.quitButton.clicked:   #if quit button was clicked
            sys.exit()
        
    def bgReset(self):
        self.background.fill((0x00, 0x00, 0x00))
        self.screen.blit(self.background, (0, 0))
    
        
        
def main():
    gui = Gui()
    gui.start() #start the gui
    
    
if __name__ == "__main__":
    main()