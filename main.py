import pygame
import random
import sys

pygame.init()

# =========================
# SCREEN
# =========================
WIDTH = 480
HEIGHT = 800
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Touch Car Racing")
clock = pygame.time.Clock()

# =========================
# COLORS
# =========================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (255, 60, 60)
BLUE = (50, 150, 255)
YELLOW = (255, 220, 0)
GREEN = (50, 255, 100)

# =========================
# ROAD
# =========================
road_x = 90
road_width = 300
line_y = 0

# =========================
# PLAYER
# =========================
player_width = 60
player_height = 110
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 150
player_speed = 8

# =========================
# ENEMIES
# =========================
enemy_width = 60
enemy_height = 110
enemy_speed = 8

lanes = [120, 210, 300]

enemies = []

# =========================
# SCORE
# =========================
score = 0
font = pygame.font.SysFont("Arial", 35)
small_font = pygame.font.SysFont("Arial", 25)

# =========================
# TOUCH BUTTONS
# =========================
left_button = pygame.Rect(20, HEIGHT - 120, 120, 90)
right_button = pygame.Rect(WIDTH - 140, HEIGHT - 120, 120, 90)

move_left = False
move_right = False

# =========================
# FUNCTIONS
# =========================
def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height), border_radius=10)

    pygame.draw.rect(screen, BLACK, (x + 8, y + 15, 15, 25), border_radius=5)
    pygame.draw.rect(screen, BLACK, (x + 37, y + 15, 15, 25), border_radius=5)

    pygame.draw.rect(screen, BLACK, (x + 10, y + 80, 12, 20), border_radius=5)
    pygame.draw.rect(screen, BLACK, (x + 38, y + 80, 12, 20), border_radius=5)


def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, enemy_width, enemy_height), border_radius=10)

    pygame.draw.rect(screen, BLACK, (x + 8, y + 15, 15, 25), border_radius=5)
    pygame.draw.rect(screen, BLACK, (x + 37, y + 15, 15, 25), border_radius=5)

    pygame.draw.rect(screen, BLACK, (x + 10, y + 80, 12, 20), border_radius=5)
    pygame.draw.rect(screen, BLACK, (x + 38, y + 80, 12, 20), border_radius=5)


def create_enemy():
    lane = random.choice(lanes)
    enemies.append([lane, -120])


def draw_road():
    global line_y

    screen.fill(GREEN)

    pygame.draw.rect(screen, GRAY, (road_x, 0, road_width, HEIGHT))

    line_y += enemy_speed
    if line_y > 80:
        line_y = 0

    for i in range(12):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, i * 80 + line_y, 10, 50))


def draw_buttons():
    pygame.draw.rect(screen, YELLOW, left_button, border_radius=20)
    pygame.draw.rect(screen, YELLOW, right_button, border_radius=20)

    left_text = font.render("LEFT", True, BLACK)
    right_text = font.render("RIGHT", True, BLACK)

    screen.blit(left_text, (left_button.x + 18, left_button.y + 25))
    screen.blit(right_text, (right_button.x + 8, right_button.y + 25))


def game_over_screen():
    while True:
        screen.fill(BLACK)

        over = font.render("GAME OVER", True, RED)
        sc = small_font.render(f"Score: {score}", True, WHITE)
        tap = small_font.render("Tap Anywhere To Restart", True, WHITE)

        screen.blit(over, (WIDTH // 2 - over.get_width() // 2, 280))
        screen.blit(sc, (WIDTH // 2 - sc.get_width() // 2, 350))
        screen.blit(tap, (WIDTH // 2 - tap.get_width() // 2, 450))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.FINGERDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return


# =========================
# MAIN LOOP
# =========================
spawn_timer = 0
running = True

while running:
    clock.tick(60)

    draw_road()

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # TOUCH DOWN
        if event.type == pygame.FINGERDOWN:
            tx = event.x * WIDTH
            ty = event.y * HEIGHT

            if left_button.collidepoint(tx, ty):
                move_left = True

            if right_button.collidepoint(tx, ty):
                move_right = True

        if event.type == pygame.FINGERUP:
            move_left = False
            move_right = False

        # MOUSE SUPPORT
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if left_button.collidepoint(mx, my):
                move_left = True

            if right_button.collidepoint(mx, my):
                move_right = True

        if event.type == pygame.MOUSEBUTTONUP:
            move_left = False
            move_right = False

    # MOVEMENT
    if move_left:
        player_x -= player_speed

    if move_right:
        player_x += player_speed

    # LIMITS
    if player_x < 105:
        player_x = 105

    if player_x > 315:
        player_x = 315

    # ENEMY SPAWN
    spawn_timer += 1

    if spawn_timer > 40:
        create_enemy()
        spawn_timer = 0

    # MOVE ENEMIES
    for enemy in enemies:
        enemy[1] += enemy_speed

    # REMOVE OFFSCREEN
    enemies = [e for e in enemies if e[1] < HEIGHT + 120]

    # DRAW ENEMIES
    for enemy in enemies:
        draw_enemy(enemy[0], enemy[1])

    # COLLISION
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)

        if player_rect.colliderect(enemy_rect):
            game_over_screen()

            enemies.clear()
            score = 0
            enemy_speed = 8
            player_x = WIDTH // 2 - player_width // 2

    # SCORE
    score += 1

    if score % 500 == 0:
        enemy_speed += 1

    # DRAW PLAYER
    draw_player(player_x, player_y)

    # DRAW BUTTONS
    draw_buttons()

    # SCORE TEXT
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    pygame.display.update()

pygame.quit()