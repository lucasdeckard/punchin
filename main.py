import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Punch-Out Game - MOO ICT 2022")

# Load the images
BACKGROUND = pygame.image.load("background.png")
PLAYER_STAND = pygame.image.load("player_stand.png")
PLAYER_LEFT_PUNCH = pygame.image.load("player_left_punch.png")
PLAYER_RIGHT_PUNCH = pygame.image.load("player_right_punch.png")
PLAYER_BLOCK = pygame.image.load("player_block.png")
ENEMY_STAND = pygame.image.load("enemy_stand.png")
ENEMY_LEFT_PUNCH = pygame.image.load("enemy_left_punch.png")
ENEMY_RIGHT_PUNCH = pygame.image.load("enemy_right_punch.png")
ENEMY_BLOCK = pygame.image.load("enemy_block.png")

# Load the font
FONT = pygame.font.SysFont("comicsansms", 32)

# Set up the game variables
player_block = False
enemy_block = False
random.seed()
enemy_speed = 5
index = 0
player_health = 100
enemy_health = 100
enemy_attacks = ["left", "right", "block"]
clock = pygame.time.Clock()

# Define the reset function
def reset_game():
    global player_health, enemy_health, enemy_speed
    player_health = 100
    enemy_health = 100
    enemy_speed = 5
    enemy_rect.centerx = 400
    enemy_rect.centery = 300
    player_rect.centerx = 200
    player_rect.centery = 300

# Set up the player sprite
player_rect = PLAYER_STAND.get_rect()
player_rect.centerx = 200
player_rect.centery = 300

# Set up the enemy sprite
enemy_rect = ENEMY_STAND.get_rect()
enemy_rect.centerx = 400
enemy_rect.centery = 300

# Set up the player health bar
player_health_bar = pygame.Rect(50, 50, player_health * 2, 30)

# Set up the enemy health bar
enemy_health_bar = pygame.Rect(550, 50, enemy_health * 2, 30)

# Set up the game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_rect = PLAYER_LEFT_PUNCH.get_rect()
                player_rect.centery = 300
                player_block = False
                if player_rect.colliderect(enemy_rect) and not enemy_block:
                    enemy_health -= 5
            elif event.key == pygame.K_RIGHT:
                player_rect = PLAYER_RIGHT_PUNCH.get_rect()
                player_rect.centery = 300
                player_block = False
                if player_rect.colliderect(enemy_rect) and not enemy_block:
                    enemy_health -= 5
            elif event.key == pygame.K_DOWN:
                player_rect = PLAYER_BLOCK.get_rect()
                player_rect.centery = 300
                player_block = True
        elif event.type == pygame.KEYUP:
            player_rect = PLAYER_STAND.get_rect()
            player_rect.centery = 300
            player_block = False

    # Move the enemy
    enemy_rect.move_ip(enemy_speed, 0)
    if enemy_rect.left > 430:
        enemy_speed = -5
    elif enemy_rect.left < 220:
        enemy_speed = 5

    #
    # Player health
    player_health = 100
    font = pygame.font.Font(None, 36)
    player_health_text = font.render("Player Health: " + str(player_health), True, (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_img = PLAYER_LEFT_PUNCH
                    player_block = False
                    if player_rect.colliderect(enemy_rect) and not enemy_block:
                        enemy_health -= 5
                elif event.key == pygame.K_RIGHT:
                    player_img = PLAYER_RIGHT_PUNCH
                    player_block = False
                    if player_rect.colliderect(enemy_rect) and not enemy_block:
                        enemy_health -= 5
                elif event.key == pygame.K_DOWN:
                    player_img = PLAYER_BLOCK
                    player_block = True

            if event.type == pygame.KEYUP:
                player_img = PLAYER_STAND
                player_block = False

        # Draw background
        SCREEN.blit(BACKGROUND, (0, 0))

        # Move the enemy
        enemy_rect.x += enemy_speed
        if enemy_rect.left > 430:
            enemy_speed = -5
        if enemy_rect.left < 220:
            enemy_speed = 5

        # Choose enemy attack
        if not enemy_attack_timer:
            enemy_attack_timer = ENEMY_ATTACK_TIMER_MAX
            enemy_attack = random.choice(["left", "right", "block"])
            if enemy_attack == "left":
                enemy_img = ENEMY_LEFT_PUNCH
                enemy_block = False
                if enemy_rect.colliderect(player_rect) and not player_block:
                    player_health -= 5
            elif enemy_attack == "right":
                enemy_img = ENEMY_RIGHT_PUNCH
                enemy_block = False
                if enemy_rect.colliderect(player_rect) and not player_block:
                    player_health -= 5
            elif enemy_attack == "block":
                enemy_img = ENEMY_BLOCK
                enemy_block = True

        # Draw the player and enemy
        SCREEN.blit(player_img, player_rect)
        SCREEN.blit(enemy_img, enemy_rect)

        # Draw health bars
        pygame.draw.rect(SCREEN, (255, 0, 0), (20, 20, player_health, 10))
        pygame.draw.rect(SCREEN, (255, 0, 0), (460, 20, enemy_health, 10))

        # Draw player health text
        SCREEN.blit(player_health_text, (20, 50))

        # Update the display
        pygame.display.update()

        # Check for end of game scenario
        if enemy_health <= 0:
            game_over("You Win!")
        elif player_health <= 0:
            game_over("You Lose!")

        # Update the enemy attack timer
        enemy_attack_timer -= 1
        if enemy_attack_timer < 0:
            enemy_attack_timer = 0
        def game_over(message):
            font = pygame.font.Font(None, 72)
            text = font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
