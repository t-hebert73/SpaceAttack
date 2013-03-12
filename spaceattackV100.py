#Filename spaceattackV100.py
#Author: Trevor Hebert
#Last Modified by: Trevor Hebert
#Date Last Modified: August 5, 2012
#Program Description: This is a simple space invaders type game where you avoid the obstacles while shooting things for points.
#Revision History: 1.0.0
#   Recently added
# - Opening game screen (GUI)
# - Basic difficultly levels
# - Scoreboard with points and lives left
# - Blackhole enemy added
#
#


import pygame, gameEngine, random, sys

#ship class
class Ship(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("ship.gif")
        self.setSpeed(0)
        self.setAngle(0)
        
        #check for key presses
    def checkEvents(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rotateBy(5)
        if keys[pygame.K_RIGHT]:
            self.rotateBy(-5)
        if keys[pygame.K_UP]:
            self.addForce(.2, self.rotation)
        if keys[pygame.K_DOWN]:
            self.addForce(-.2, self.rotation)
        if keys[pygame.K_SPACE]:
            self.scene.bullet.fire()

           
    
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
        self.setImage("rock.gif")
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
        self.setImage("rock.gif")
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

        
#easygame class        
class easyGame(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self)
        self.ship = Ship(self)
        self.bullet = Bullet(self)
        self.scoreboard = gameEngine.Label()
        self.scoreboard.center = (500, 20)
        self.scoreboard.size = (250,30)
        self.scoreboard.bgColor = (0x00, 0x00, 0x00)
        self.scoreboard.fgColor = (0xCC, 0xCC, 0xCC)
        
        self.score = 0  #player score
        self.lives = 5 #player lives
        
        #create list of rocks
        self.rocks = []
        for i in range(4): #make 10 rocks
            self.rocks.append(Rock(self))
         
        self.rockGroup = self.makeSpriteGroup(self.rocks)
        self.addGroup(self.rockGroup)
        self.sprites = [self.bullet, self.ship, self.scoreboard]
        self.setCaption("Space Attack")       
        
        
    def update(self):
        self.updateScore()
        
        rockHitShip = self.ship.collidesGroup(self.rocks)
        if rockHitShip:
            rockHitShip.reset()
            self.lives -= 1

        rockHitBullet = self.bullet.collidesGroup(self.rocks)
        if rockHitBullet:
            rockHitBullet.reset()
            self.bullet.reset()
            self.score += 100
            
        if self.lives == 0:
            self.stop()
            endGui = Gui()
            endGui.start()   
        
     
        
    def updateScore(self):
        score = "Score: %.0f Lives: %.0f" % (self.score, self.lives)
        self.scoreboard.text = score   
  
#mediumgame class        
class mediumGame(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self)
        self.ship = Ship(self)
        self.bullet = Bullet(self)
        self.blackhole = Blackhole(self)
        self.scoreboard = gameEngine.Label()
        self.scoreboard.center = (500, 20)
        self.scoreboard.size = (250,30)
        self.scoreboard.bgColor = (0x00, 0x00, 0x00)
        self.scoreboard.fgColor = (0xCC, 0xCC, 0xCC)
        
        self.score = 0  #player score
        self.lives = 5 #player lives
        
        #create list of rocks
        self.rocks = []
        for i in range(8): #make 8 rocks
            self.rocks.append(Rock(self))
        #create list of blackholes
        self.blackholes = []
        for i in range(3): #make 3 blackholes
            self.blackholes.append(Blackhole(self))    
         
        self.rockGroup = self.makeSpriteGroup(self.rocks)
        self.blackholeGroup = self.makeSpriteGroup(self.blackholes)
        self.addGroup(self.rockGroup)
        self.addGroup(self.blackholeGroup)
        self.sprites = [self.bullet, self.ship, self.scoreboard, self.blackhole]
        self.setCaption("Space Attack")       
        
        
    def update(self):
        self.updateScore()
        
        #if a rock hits the ship
        rockHitShip = self.ship.collidesGroup(self.rocks)
        if rockHitShip:
            rockHitShip.reset()
            self.lives -= 1
            
        #if a blackhole hits the ship    
        blackholeHitShip = self.ship.collidesGroup(self.blackholes)
        if blackholeHitShip:
            blackholeHitShip.reset()
            self.lives -= 1   

        rockHitBullet = self.bullet.collidesGroup(self.rocks)
        if rockHitBullet:
            rockHitBullet.reset()
            self.bullet.reset()
            self.score += 100
     
        if self.lives == 0:
            self.stop()
            endGui = Gui()
            endGui.start()
     
    def updateScore(self):
        score = "Score: %.0f Lives: %.0f" % (self.score, self.lives)
        self.scoreboard.text = score   
     
#hardgame class        
class hardGame(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self)
        self.ship = Ship(self)
        self.bullet = Bullet(self)
        self.blackhole = Blackhole(self)
        self.scoreboard = gameEngine.Label()
        self.scoreboard.center = (500, 20)
        self.scoreboard.size = (250,30)
        self.scoreboard.bgColor = (0x00, 0x00, 0x00)
        self.scoreboard.fgColor = (0xCC, 0xCC, 0xCC)
        
        self.score = 0  #player score
        self.lives = 5 #player lives
        
        #create list of rocks
        self.rocks = []
        for i in range(12): #make 10 rocks
            self.rocks.append(Rock(self))
            
        #create list of blackholes    
        self.blackholes = []
        for i in range(3): #make 3 blackholes
            self.blackholes.append(Blackhole(self))        
         
        self.rockGroup = self.makeSpriteGroup(self.rocks)
        self.blackholeGroup = self.makeSpriteGroup(self.blackholes)
        self.addGroup(self.rockGroup)
        self.addGroup(self.blackholeGroup)
        self.sprites = [self.bullet, self.ship, self.scoreboard]
        self.setCaption("Space Attack")       
        
        
    def update(self):
        self.updateScore()
        
        rockHitShip = self.ship.collidesGroup(self.rocks)
        if rockHitShip:
            rockHitShip.reset()
            self.lives -= 1

        rockHitBullet = self.bullet.collidesGroup(self.rocks)
        if rockHitBullet:
            rockHitBullet.reset()
            self.bullet.reset()
            self.score += 100
            
        #if a blackhole hits the ship    
        blackholeHitShip = self.ship.collidesGroup(self.blackholes)
        if blackholeHitShip:
            blackholeHitShip.reset()
            self.lives -= 1      
     
        if self.lives == 0:
            self.stop()
            endGui = Gui()
            endGui.start()
     
    def updateScore(self):
        score = "Score: %.0f Lives: %.0f" % (self.score, self.lives)
        self.scoreboard.text = score   
        



class Gui(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self)
        #initialize background to black
        self.background.fill((0x00, 0x00, 0x00))
        self.setCaption("Space Attack!") 
        self.addLabels()
        self.addButtons()
        
        self.sprites = [self.label, self.easyButton, self.mediumButton, self.hardButton, self.quitButton]
    
    def addLabels(self):    #create title label
        self.label = gameEngine.Label()
        self.label.font = pygame.font.Font("goodfoot.ttf", 40)
        self.label.text = "Space Attack!"
        self.label.fgColor = (0xCC, 0xCC, 0xCC)
        self.label.bgColor = (0x00, 0x00, 0x00)
        self.label.center = (320, 100)
        self.label.size = (200, 50)
        
    def addButtons(self):   #add the GUI buttons
        self.easyButton = gameEngine.Button()
        self.easyButton.center = (250, 180)
        self.easyButton.text = "Easy"   #easy button
        
        self.mediumButton = gameEngine.Button()
        self.mediumButton.center = (450, 180)
        self.mediumButton.text = "Medium"   #medium button
        
        self.hardButton = gameEngine.Button()
        self.hardButton.center = (250, 380)
        self.hardButton.text = "Hard"   #hard button
        
        self.quitButton = gameEngine.Button()
        self.quitButton.center = (450, 380)
        self.quitButton.text = "Quit Game"  #quit button
        
    def update(self):        
        if self.easyButton.clicked: #if easy button was clicked
            game = easyGame()
            game.start()
        if self.mediumButton.clicked: #if medium button was clicked
            game = mediumGame()
            game.start()
        if self.hardButton.clicked: #if hard button was clicked
            game = hardGame()
            game.start()        
            
        elif self.quitButton.clicked:   #if quit button was clicked
            sys.exit()
    
        
        
def main():
    gui = Gui()
    gui.start() #start the gui
    
    
if __name__ == "__main__":
    main()