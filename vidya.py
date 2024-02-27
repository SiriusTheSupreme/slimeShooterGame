# init lines
import pygame, math
from random import randint
pygame.init()

# preparation
screenWide = 500
screenHigh = 500
screen = pygame.display.set_mode([screenWide, screenHigh])
pygame.display.set_caption("Slimes have guns??") 
pygame.mouse.set_visible(False)

# character
invFrames
playerHP = 10
playerX = 200
playerY = 200
cursorSprite = pygame.image.load('cursor.png')
charSprite = pygame.image.load('slime.png')
gunSprite = pygame.image.load('gun.png')
bulletSprite = pygame.image.load('bullet.png')
speed = 1
jump = 1
jumpLimit = 1
jumpPower = 100
jumpDistanceRemaining = 0
jumping = False
crashdownSpeed = 3
shooting = False

cursor_pos = list(screen.get_rect().center)

# bullet class
class playerBullet(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = pygame.transform.smoothscale(pygame.image.load('bullet.png'), (51, 51))
        self.vel = 1
        
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.x, my - self.y
        len = math.hypot(dx, dy)
        self.dx = dx / len
        self.dy = dy / len

        angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.image = pygame.transform.rotate(self.image, angle)

    def move(self):
        self.x += self.dx * self.vel
        self.y += self.dy * self.vel

    def draw(self,screen):
        screen.blit(self.image, (round(self.x), round(self.y)))

# bullet storage
bullets = []
shoot_loop = 0

bossHP = 100

# first boss
class bossDrone(object):
    def __init__(self,x,y,screenWidth):
        self.x = x
        self.y = y
        self.direction = 5
        self.xLimit = screenWidth - 200
        self.image = pygame.transform.smoothscale(pygame.image.load('drone.png'), (200, 74))
        
    def movements(self):
        self.x += self.direction
        # Move towards the player horizontally
        
    def dirChange(self, playerXpos):
        if self.x + 20 < playerX:
            self.direction = 2  # Direction change
        elif self.x + 20 > playerX:
            self.direction = -2 # Direction change
    
    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))
    
    def attack(self, playerXpos):
        # Release bomb when positioned above the player
        if abs(self.x - playerX) < 40:
            bombs.append(droneBomb(self.x + 80, self.y + 74))
            
class droneBomb(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.transform.smoothscale(pygame.image.load('shell.png'), (50, 166))
        self.vel = 1

    def move(self):
        self.y += self.vel

    def draw(self, screen):
        screen.blit(self.image, (round(self.x), round(self.y)))

# main loop
bombs = []
clock = pygame.time.Clock()
currentBoss = 1
droneBoss = bossDrone(100, 20, screenWide)
isRun = True
canSpawnBoss = False
bossSpawnCooldown = 1000
while isRun:
    
    # screen bg
    screen.fill((255, 255, 255))

    # removes invulnerability frames
    if invFrames > 0:
        invFrames -= 1
    
    # checks if a boss can be spawned
    if canSpawnBoss == True:
        bossSpawnCooldown -= 1
        if bossSpawnCooldown == 0:
            print("You won!")
            canSpawnBoss = False
    else:
        bossSpawnCooldown = 1000
    
    # bosses
    if currentBoss == 1:
        droneBoss.movements()
        droneBoss.draw(screen)
        if bossHP >= 50:
            if randint(1,20) == 2:
                droneBoss.dirChange(playerX)
            if randint(1,200) == 5:
                droneBoss.attack(playerX)
        elif bossHP <= 50:
            if randint(1,70) == 2:
                droneBoss.dirChange(playerX)
            if randint(1,50) == 5:
                droneBoss.attack(playerX)
        for bomb in bombs:
            bomb.move()
            bomb.draw(screen)
            # collision detect
            if (bomb.x > playerX and bomb.x < playerX + 100 and bomb.y > playerY and bomb.y < playerY + 100) and invFrames == 0:
                playerHP -= 1
                invFrames = 600
                bombs.pop(bombs.index(bomb))
            
    
    # kills bullets if they move out of bounds
    for bullet in bullets:       
        if -50 < bullet.x < screenWide and -50 < bullet.y < screenWide:
            bullet.move()
        else:
            bullets.pop(bullets.index(bullet)) 
    
    # mouse locator for gun, I will NOT be fixing this buggy mess
    mouseX, mouseY = pygame.mouse.get_pos()
    rel_x, rel_y = mouseX - playerX, mouseY - playerY
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    rotimage = pygame.transform.rotate(gunSprite,angle)
    
    
    # flawless gravity system
    if jumpDistanceRemaining >= 0:
        playerY = playerY - 2
        jumpDistanceRemaining = jumpDistanceRemaining - 1
    if playerY <= screenHigh - 100:
        playerY = playerY + 1
    if playerY >= screenHigh - 100 and jumping == False:
        playerY = screenHigh - 100
    
    # jump reload
    if jump != jumpLimit and playerY == screenHigh - 100: 
        jump = jump + 1
    
    # event grabber
    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT or playerHP == 0:
            isRun = False
        # i want to kill myself
        elif event.type == pygame.MOUSEBUTTONDOWN:
            shooting = True
        elif event.type == pygame.MOUSEBUTTONUP:
            shooting = False
            
    
    # input grabber
    key = pygame.key.get_pressed()
    
    # shmovement
    if key[pygame.K_a] and playerX > 0:
        playerX = playerX - speed
    if key[pygame.K_d] and playerX < screenWide - 100:
        playerX = playerX + speed
    
    # intricate jump mechanics
    if key[pygame.K_SPACE]:
        if playerY >= (screenHigh - 100):
            if jump != 0:
                jump = jump - 1
                jumping = True
                jumpDistanceRemaining = jumpDistanceRemaining + jumpPower
                floorReached = False
    if key[pygame.K_s] and playerY < screenHigh - 100:
        playerY = playerY + 2
        jumpDistanceRemaining = 0
    
    # shoot speed
    if shoot_loop > 0:
        # increase "0.02" to your liking
        shoot_loop += 0.02
    if shoot_loop > 3:
        shoot_loop = 0
    
    # the code that actually shoots the bullets
    if shooting and shoot_loop == 0:
        if len(bullets) < 100:
            bullets.append(playerBullet(round(playerX + 20), round(playerY + 20),))

        shoot_loop = 1
    
    # character boi
    rect = rotimage.get_rect(center=(playerX+50 ,playerY+50))
    screen.blit(rotimage,rect)
    screen.blit(charSprite, (playerX, playerY))
    screen.blit(cursorSprite, (mouseX + 10, mouseY + 10)) 

    # the code that displays the bullets and detects collisions
    for bullet in bullets:
        bullet.draw(screen)
        if currentBoss == 1:
            if bullet.x < droneBoss.x + 200 and bullet.x > droneBoss.x and bullet.y < droneBoss.y + 74 and bullet.y > droneBoss.y:
                bossHP -= 1
                bullets.pop(bullets.index(bullet)) 
    
    if bossHP == 0:
        currentBoss += 1
        canSpawnBoss = True
    
    # uptate screen
    pygame.display.flip()
quit()
