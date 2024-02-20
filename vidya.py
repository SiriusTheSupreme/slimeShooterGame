# init lines
import pygame, math
pygame.init()

# preparation
screenWide = 500
screenHigh = 500
screen = pygame.display.set_mode([screenWide, screenHigh])
pygame.display.set_caption("Slimes have guns??") 
pygame.mouse.set_visible(False)

# character
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
crashdownSpeed = 1
shooting = False

cursor_pos = list(screen.get_rect().center)

# bullet class
class playerBullet(object):
    def __init__(self,x,y,radius,color):
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

    def draw(self,win):
        win.blit( self.image, (round(self.x), round(self.y)))

# bullet storage
bullets = []
shoot_loop = 0

# main loop
pygame.display.flip()
isRun = True
while isRun:
    
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
        if event.type == pygame.QUIT:
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
        if playerY >= 400:
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
            bullets.append(playerBullet(round(playerX + 20), round(playerY + 20), 6, (255,255,255)))

        shoot_loop = 1
       
    # screen bg
    screen.fill((255, 255, 255))
    
    # character boi
    rect = rotimage.get_rect(center=(playerX+50 ,playerY+50))
    screen.blit(rotimage,rect)
    screen.blit(charSprite, (playerX, playerY))
    screen.blit(cursorSprite, (mouseX + 10, mouseY + 10))

    # the code that displays the bullets
    for bullet in bullets:
        bullet.draw(screen)
    
    # uptate screen
    pygame.display.flip()
        
quit()