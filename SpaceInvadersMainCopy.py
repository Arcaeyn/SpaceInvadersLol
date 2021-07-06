from sys import exit
import pygame
import random
import math
import time



from pygame import mixer

# Get Functions
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("space-invaders.png")
pygame.display.set_icon(icon)

# Background
listx = []
listy = []
listt = []

# Background Music
mixer.music.load("background-music.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.3)

for num in range(1, 202):
    x = random.randint(0, 800)
    y = random.randint(0, 600)
    t = random.randint(1, 4)
    listx.append(x)
    listy.append(y)
    listt.append(t)
    
    
def draw_stars(screen):
    global listy
    global listx
    global listt
    for idx in range(1, 200):
        x = listx[idx]
        y = listy[idx]
        t = listt[idx]


      
        listy[idx] = listy[idx] + 1.3
            
        
        if listy[idx] > 602:
            listy[idx] = -1
            
        if idx > 180:
            pygame.draw.circle(screen, "red", (x,y), t, t)

        elif idx < 50:
            pygame.draw.circle(screen, "white", (x,y), 0.05, t)

        else:
            pygame.draw.circle(screen, "white", (x,y), t, t)

    
        
#background = pygame.image.load("space-invaders-bg.jpg")
#background2 = pygame.image.load("space-invaders-bg3.jpg")
#switch = random.randint(0, 3)

# Player
playerImg = pygame.image.load("player-64-bit.png")
playerX = 370
left = False
playerY = 480
right = False
playerChange = 0
playerDeath = False

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyChange = []
dead = []
numEnemies = 6
greater = 0
greater1 = 0

# Extra Mechanics
maxhits = 1
hits = []
totalhits = 0
enemySpeed = 0
counter = False
enemyLives = 1
counter1 = 2

for i in range(numEnemies):

    if greater + 130 > 800:
        greater = 0
        greater1 = greater1 + 65

    enemyImg.append(pygame.image.load("ufo.png"))
    enemyX.append(15 + greater)
    enemyY.append(50 + greater1)
    enemyChange.append(0.1)
    greater = greater + 130
    dead.append(False)
    hits.append(0)


# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 370
bulletY = 480
bulletChange = 0.7
bulletState = "ready"
startpos = playerX



# Score
scoreship = 0
scoreValue = 100
font = pygame.font.Font("C:\WINDOWS\FONTS\COURBD.TTF", 20)
file = open("high-score.txt")
highscore = int(file.readline())
print(highscore)
file.close()

scoreX = 15
scoreY = 10

# End Game
endX = 144
endY = 300
endImg = pygame.image.load("game-over.png")

# Clock
clock = pygame.time.Clock()

wave1 = 1
waveX = 350
waveY = 10

    
def print_score(x, y, i, j, a, b):
    global wave
    score = font.render("Score: " + ("{:,}".format(scoreship)), True, (255, 255, 255))
    lives = font.render("Enemy Lives: " + str(int(maxhits)), True, (255, 255, 255))
    wave = font.render("Wave: " + str(wave1), True, (255, 255, 255))
    highscoref = "{:,}".format(highscore)
    highscore1 = font.render("Highscore: " + str(highscoref), True, (255, 255, 255))

    screen.blit(wave, (a, b))
    screen.blit(lives, (i, j))
    screen.blit(score, (x, y))
    screen.blit(highscore1, (scoreX,35))


def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

    
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(bulletY - enemyY, 2)))

    if distance < 45:
        return True
    else:
        return False


    
def enemy(x, y, i):
    global enemyImg
    screen.blit(enemyImg[i], (x, y))
    

def player(x, y):
    screen.blit(playerImg, (x, y))

    
# Game Loop
while playerDeath == False:
    dt = clock.tick(60)
    
    screen.fill((20, 15, 40))
    #if switch == 0:
       # screen.blit(background, (0, 0))


    #else:
     #   screen.blit(background2, (0, 0))

    
    draw_stars(screen)

        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerChange = -0.35
                left = True

            if event.key == pygame.K_RIGHT:
                playerChange = 0.35
                right = True

            if event.key == pygame.K_SPACE and bulletState == "ready":
                fire_bullet(playerX, bulletY)
                startpos = playerX
                bulletSound = mixer.Sound("lazer.wav")
                bulletSound.set_volume(0.1)
                bulletSound.play()
                


        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                left = False
                
                if right == True:
                    playerChange = 0.35

                else:
                    playerChange = 0

            elif event.key == pygame.K_RIGHT:
                right = False
                
                if left == True:
                    playerChange = -0.35

                else:
                    playerChange = 0
                 
            
    if playerX + playerChange * dt < 735 and playerX + playerChange  * dt > 5:
        playerX += playerChange * dt


    if bulletY <= 0:
        bulletState = "ready"
        bulletY = 480

    if bulletState == "fire":
            fire_bullet(startpos, bulletY)
            bulletY -= 0.6 * dt
    if scoreship > highscore:
        highscore = scoreship
        
        file = open("high-score.txt", "w")
        file.write(str(highscore))
        file.close
    
    if totalhits == numEnemies:
   
        scoreValue += 50
        enemyX = []
        enemyY = []
        dead = []
        hits = []
        totalhits = 0
        maxhits += 0.2
        greater = 0
        greater1 = 0
        enemyChange = []
        enemySpeed += 0.03
        enemyLives = int(maxhits)
        wave1 += 1

        
        
        if enemyLives == counter1:
            
            counter1 += 1
            counter = True
            
        if counter == True:
            
            enemySpeed = 0

        counter = False

            

        
        
        for i in range(numEnemies):
            
            if greater + 130 > 800:
                greater = 0
                greater1 = greater1 + 65

            enemyX.append(15 + greater)
            enemyY.append(50 + greater1)
            greater = greater + 130
            dead.append(False)
            hits.append(0)
            enemyChange.append(0.1 + enemySpeed)

        

    
    for i in range(numEnemies):

        if isCollision(enemyX[i], enemyY[i], playerX, playerY):
            playerDeath = True
        
        if isCollision(enemyX[i], enemyY[i], startpos, bulletY) == True and bulletState == "fire":
            
            if dead[i] == False:
                bulletY = 480
                bulletState = "ready"
                
                hits[i] += 1

                if hits[i] == int(maxhits):
                    scoreship = scoreship + scoreValue
                    dead[i] = True
                    totalhits = totalhits + 1
                    

        if dead[i] == False:
            enemyX[i] = enemyX[i] + (enemyChange[i] * dt)
            enemy(enemyX[i], enemyY[i], i)
         
        
        if enemyX[i] + enemyChange[i] * dt >= 740:
            enemyChange[i] = enemyChange[i] * -1
            enemyY[i] = enemyY[i] + 65

        elif enemyX[i] + enemyChange[i] * dt <= 5:
            enemyChange[i] = enemyChange[i] * -1
            enemyY[i] = enemyY[i] + 65
        
    
    
    
        
         
    player(playerX, playerY)
    print_score(scoreX, scoreY, 600, 15, waveX, waveY)
    pygame.display.update()
    


screen.fill((20, 30, 70))    

draw_stars(screen)

file = open("high-score.txt", "w")
file.write(str(highscore))
file.close
print(highscore)
screen.blit(endImg, (150, 50))
print_score(scoreX, scoreY, 600, 15, waveX, waveY)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

            mixer.music.pause()
            
