import pygame
import random
import sys

pygame.init()

# Arguments
WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (0, 0, 50)

playerSize = 50
playerPos = [WIDTH/2, HEIGHT - 2 * playerSize]

enemySize = 50
enemy_pos = [random.randint(0, WIDTH-enemySize), 0]
enemy_list = [enemy_pos]

SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont('monospace', 35)


def set_level(score, SPEED):
    if score < 40:
        SPEED = 5
    elif score < 80:
        SPEED = 10
    elif score < 140:
        SPEED = 15
    elif score < 200:
        SPEED = 20
    else:
        SPEED = 30

    return SPEED


# Droping enemies on the screen
def dorp_enemies(enemy_list):
    deley = random.random()
    if len(enemy_list) < 10 and deley < 0.3:
        x_pos = random.randint(0, WIDTH-enemySize)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

# This function drawing enemies on the screen


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemySize, enemySize))

# Updateing enemy's position


def update_enemy_position(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score

# checking collision


def collider(enemy_list, playerPos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, playerPos):
            return True
    return False

# Detect collision of player and enemy


def detect_collision(playerPos, enemy_pos):
    p_x = playerPos[0]
    p_y = playerPos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + playerSize)) or (p_x >= e_x and p_x < (e_x + enemySize)):
        if(e_y >= p_y and e_y < (p_y + playerSize)) or (p_y >= e_y and p_y < (e_y + enemySize)):
            return True

    return False


# Game loop
while not game_over:
    # Player movment
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            x = playerPos[0]
            y = playerPos[1]

            if event.key == pygame.K_LEFT:
                x -= playerSize
            elif event.key == pygame.K_RIGHT:
                x += playerSize

            playerPos = [x, y]

    screen.fill(BACKGROUND_COLOR)

    # Drawing player
    pygame.draw.rect(screen, RED, (playerPos[0], playerPos[1], playerSize, playerSize))

    # enemy's functions
    dorp_enemies(enemy_list)
    score = update_enemy_position(enemy_list, score)
    SPEED = set_level(score, SPEED)

    text = "Score: " + str(score)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH-200, HEIGHT-40))

    if collider(enemy_list, playerPos):
        game_over = True

    draw_enemies(enemy_list)

    print(SPEED)

    # Update display
    clock.tick(30)

    pygame.display.update()
