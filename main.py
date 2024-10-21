import math
import random
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change =0

# Enemy
num_of_enemies = 36  # Total enemies
rows = 4           # Number of rows
cols = 9             # Number of columns

# Ensure the total number of enemies matches rows * cols
assert num_of_enemies == rows * cols, "Number of enemies must match rows * columns."

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

# Initialize enemies in a grid formation
horizontal_spacing = 80  # Decrease this value to reduce horizontal spacing
vertical_spacing = 60    # Decrease this value to reduce vertical spacing

for row in range(rows):
    for col in range(cols):
        index = row * cols + col
        enemyImg.append(pygame.image.load('enemy.png'))
        enemyX.append(col * horizontal_spacing)  # Adjust horizontal spacing
        enemyY.append(row * vertical_spacing + 50)  # Adjust vertical spacing
        enemyX_change.append(4)
        enemyY_change.append(20)


# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Buttons
button_font = pygame.font.Font('freesansbold.ttf', 48)
play_button_rect = pygame.Rect(300, 250, 200, 100)  
replay_button_rect = pygame.Rect(300, 350, 200, 100) 
close_button_rect = pygame.Rect(300, 460, 200, 100)  

# Load Button Images
replay_button_img = pygame.image.load('rp.png')  # Load your replay image here
replay_button_img = pygame.transform.scale(replay_button_img, (200, 100))  # Scale as needed

close_button_img = pygame.image.load('close.png')  # Load your close image here
close_button_img = pygame.transform.scale(close_button_img, (200, 100))  

# Play Button Image
play_button_img = pygame.image.load('R.png')  
play_button_img = pygame.transform.scale(play_button_img, (200, 100))  

def reset_game():
    global playerX, playerY, playerX_change
    global enemyX, enemyY, enemyX_change, enemyY_change
    global bulletY, bullet_state, score_value

    playerX = 370
    playerY = 480
    playerX_change = 0
    bulletY = 480
    bullet_state = "ready"
    score_value = 0

    for i in range(num_of_enemies):
        enemyX[i] = (i % cols) * (800 // cols)  # Reset x position in grid
        enemyY[i] = (i // cols) * (600 // (rows + 1))  # Reset y position in grid

# Functions
# Functions
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    # Display the score above the game over text
    score_text = font.render("Your Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score_text, (300, 200))  # Position above the game over text

    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))  # Position below the game over text

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

def draw_play_button():
    screen.blit(play_button_img, (play_button_rect.x, play_button_rect.y))  # Draw play button image

def draw_replay_close_buttons():
    screen.blit(replay_button_img, (replay_button_rect.x, replay_button_rect.y))
    screen.blit(close_button_img, (close_button_rect.x, close_button_rect.y))

# Game Loop
running = True
game_started = False
game_over = False

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))#FOR BACKGROUNG IMAGE

    if not game_started:
        draw_play_button()  # Show play button image
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game_started = True  # Start the game

    elif game_over:
        game_over_text()
        draw_replay_close_buttons()  # Show replay and close buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button_rect.collidepoint(event.pos):
                    reset_game()
                    game_over = False  # Restart the game
                if close_button_rect.collidepoint(event.pos):
                    running = False  # Close the game
#MOVEMENT OF PLAYER UP , DOWN , WRITE AND LEFT
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_UP:
                    playerY_change = -5
                if event.key == pygame.K_DOWN:
                    playerY_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        playerX += playerX_change
        playerY += playerY_change
        playerX = max(0, min(playerX, 736))
        playerY = max(0, min(playerY, 550)) 
#ENEMY MOVEMENT
        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                game_over = True  
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, testY)

    pygame.display.update()
