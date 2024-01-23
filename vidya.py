# init lines
import pygame, math
pygame.init()

# prep
screenWide = 500
screenHigh = 500
screen = pygame.display.set_mode([screenWide, screenHigh])
pygame.display.set_caption("Slimes have guns??") 

# character
playerX = 200
playerY = 200
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
bulletSpeed = 2
allBullets = []

# main loop
pygame.display.flip()
isRun = True
while isRun:
    # mouse locator
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
            print("0")
            distanceX = mouseX - playerX
            distanceY = mouseY - playerY
            angleBu = math.atan2(distanceY, distanceX)
            bulletSpeedX = bulletSpeed * math.cos(angleBu)
            bulletSpeedY = bulletSpeed * math.sin(angleBu)
            allBullets.append([playerX, playerY, bulletSpeedX, bulletSpeedY])
            print("1")
            
    
    for item in allBullets:
        item[0] += item[2]
        item[1] += item[3] 
    
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
       
    # screen bg
    screen.fill((255, 255, 255))
    
    # character boi
    rect = rotimage.get_rect(center=(playerX+50 ,playerY+50))
    screen.blit(rotimage,rect)
    screen.blit(charSprite, (playerX, playerY))
    
    for pos_x, pos_y, bulletSpeedX, bulletSpeedY in allBullets:
        pos_x = int(pos_x)
        pos_y = int(pos_y)
        pygame.draw.line(screen, (0,255,0), (pos_x, pos_y), (pos_x, pos_y))
    
    # uptate screen
    pygame.display.flip()
        
quit()