import pygame
import random
import math

#initialising pygame. below line is comulsory to use to initiate the pygame
pygame.init()

#create screen , 800-height of pixel, 600-width of pixel
screen=pygame.display.set_mode((800, 600))

#background
background = pygame.image.load("background.png")
#title and icon
pygame.display.set_caption("Space Invaders")
icon= pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load("spaceship.png")
playerX= 370
playerY= 480
playerX_change=0 

#enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0,735)) #we used random library so that enemy can change its position by getting respwan
    enemyY.append(random.randint(100,150))
    enemyX_change.append(0.3)
    enemyY_change.append(35)

#bullet
bulletImg=pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=1
bullet_state ="ready" #ready state means you cant see the bullet on the screen
                      #fire state means the bullet is currently moving 

#score
score_value= 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

#game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x,y):
    score=font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("Game Over", True, (255,255,255))
    screen.blit(over_text, (200, 250))

def player(x,y):     #blit means to draw
    screen.blit(playerImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state= "fire"
    screen.blit(bulletImg, (x + 16 ,y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance= math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


#game loop is while loop below
#for starting and closing the window
running=True
while running:

    #RGB=RED,GREEN,BLUE
    screen.fill((50,50,50))
    
    #background
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #if keystroke is pressed check whether it is right or left 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3 
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    #gets the current coordinate of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        #to know that keystroke is removed or not        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_change=0 #spaceship stops on removing hand from keys

                              
    #for boundaries of player's spaceship
    playerX += playerX_change
    
    if playerX <=0:
        playerX = 0
    elif playerX >=736: #here we took 736 because size of spaceship is 64 pixels so we subtract size(width) os spaceship from total width of screen i.e 800
        playerX = 736
    
    #for boundary of alien
    for i in range(num_of_enemies): 

        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i]= 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i]= -0.3
            enemyY[i] += enemyY_change[i]
        
        #collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY= 480
            bullet_state = "ready"
            score_value += 1
            print(score_value) 
            enemyX[i]=random.randint(0,735) #enemy gets respwan to new place after getting hit by bullet   
            enemyY[i]=random.randint(100,150)
    
        enemy(enemyX[i], enemyY[i], i )  
    #bullet movement 
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX , bulletY )
        bulletY -= bulletY_change
    
    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()#this line is compulsary to update the screen after each event taking place in game.So it is compulsory to use it.
