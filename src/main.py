import pygame
import math
import random
import time

# Spielfigur Position
player_pos = [100, 100]
player_size = 50
player_color = (255, 255, 0)  # Gelb

# Fenstergröße
window_size = (800, 600)

# Wände Positionen
walls = [
    pygame.Rect(200, 150, 50, 200),
    pygame.Rect(400, 150, 50, 200),
    pygame.Rect(600, 150, 50, 200)
]

# Gegner Positionen und Farben
enemies = [
    {"pos": [300, 300], "color": (255, 0, 0), "chase_timer": 1, "is_chasing": False, "move_timer": 0, "direction": (0, 0)},
    {"pos": [500, 300], "color": (0, 255, 0), "chase_timer": 3, "is_chasing": False, "move_timer": 0, "direction": (0, 0)},
    {"pos": [700, 300], "color": (0, 0, 255), "chase_timer": 5, "is_chasing": False, "move_timer": 0, "direction": (0, 0)}
]

chase_duration = 5
chase_interval = 5
move_interval = 1  # 1 second for each direction

# Punkte Positionen
dots = [[x, y] for x in range(50, window_size[0], 100) for y in range(50, window_size[1], 100)]
score = 0

def draw_grid(screen):
    grid_color = (200, 200, 200)
    for x in range(0, window_size[0], 50):
        pygame.draw.line(screen, grid_color, (x, 0), (x, window_size[1]))
    for y in range(0, window_size[1], 50):
        pygame.draw.line(screen, grid_color, (0, y), (window_size[0], y))

def draw_walls(screen):
    wall_color = (0, 0, 255)
    for wall in walls:
        pygame.draw.rect(screen, wall_color, wall)

def draw_player(screen):
    # Zeichne einen 7/8 Kreis
    center = (player_pos[0] + player_size // 2, player_pos[1] + player_size // 2)
    radius = player_size // 2
    start_angle = 0
    end_angle = 315  # 7/8 Kreis
    pygame.draw.arc(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size), math.radians(start_angle), math.radians(end_angle), radius)
    pygame.draw.line(screen, player_color, center, (center[0] + radius * math.cos(math.radians(start_angle)), center[1] - radius * math.sin(math.radians(start_angle))), radius)
    pygame.draw.line(screen, player_color, center, (center[0] + radius * math.cos(math.radians(end_angle)), center[1] - radius * math.sin(math.radians(end_angle))), radius)

def draw_enemies(screen):
    for enemy in enemies:
        pygame.draw.circle(screen, enemy["color"], enemy["pos"], player_size // 2)

def draw_dots(screen):
    dot_color = (255, 255, 0)  # Gelb
    for dot in dots:
        pygame.draw.circle(screen, dot_color, dot, 5)

def move_enemies():
    current_time = time.time()
    for enemy in enemies:
        if enemy["is_chasing"]:
            if current_time - enemy["chase_timer"] > chase_duration:
                enemy["is_chasing"] = False
                enemy["chase_timer"] = current_time
        else:
            if current_time - enemy["chase_timer"] > chase_interval:
                enemy["is_chasing"] = True
                enemy["chase_timer"] = current_time

        if enemy["is_chasing"]:
            direction_x = player_pos[0] - enemy["pos"][0]
            direction_y = player_pos[1] - enemy["pos"][1]

            if abs(direction_x) > abs(direction_y):
                direction_x = 1 if direction_x > 0 else -1
                direction_y = 0
            else:
                direction_x = 0
                direction_y = 1 if direction_y > 0 else -1

            new_pos = [enemy["pos"][0] + direction_x * 5, enemy["pos"][1] + direction_y * 5]
        else:
            if current_time - enemy["move_timer"] > move_interval:
                enemy["direction"] = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                enemy["move_timer"] = current_time

            new_pos = [enemy["pos"][0] + enemy["direction"][0] * 5, enemy["pos"][1] + enemy["direction"][1] * 5]

        enemy_rect = pygame.Rect(new_pos[0], new_pos[1], player_size, player_size)
        if not any(enemy_rect.colliderect(wall) for wall in walls) and 0 <= new_pos[0] <= window_size[0] - player_size and 0 <= new_pos[1] <= window_size[1] - player_size:
            enemy["pos"] = new_pos

def handle_input():
    global score
    keys = pygame.key.get_pressed()
    new_pos = player_pos[:]
    if keys[pygame.K_LEFT]:
        new_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        new_pos[0] += 5
    if keys[pygame.K_UP]:
        new_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        new_pos[1] += 5

    # Kollisionsabfrage mit Wänden
    player_rect = pygame.Rect(new_pos[0], new_pos[1], player_size, player_size)
    if not any(player_rect.colliderect(wall) for wall in walls) and 0 <= new_pos[0] <= window_size[0] - player_size and 0 <= new_pos[1] <= window_size[1] - player_size:
        player_pos[0], player_pos[1] = new_pos

    # Kollisionsabfrage mit Punkten
    for dot in dots[:]:
        if player_rect.collidepoint(dot):
            dots.remove(dot)
            score += 1

    # Kollisionsabfrage mit Gegnern
    if any(player_rect.colliderect(pygame.Rect(enemy["pos"][0], enemy["pos"][1], player_size, player_size)) for enemy in enemies):
        reset_game()

    # Cheat: Move all enemies to the bottom right corner and stop their movement
    if keys[pygame.K_z]:
        for enemy in enemies:
            enemy["pos"] = [window_size[0] - player_size, window_size[1] - player_size]
        enemies.clear()  # Clear the enemies list to stop their movement

def show_winning_screen(screen):
    font = pygame.font.Font(None, 74)
    text = font.render("You Win!", True, (255, 255, 255))
    screen.blit(text, (window_size[0] // 2 - text.get_width() // 2, window_size[1] // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

def reset_game():
    global player_pos, dots, score
    player_pos = [100, 100]
    dots = [[x, y] for x in range(50, window_size[0], 100) for y in range(50, window_size[1], 100)]
    score = 0
    for enemy in enemies:
        enemy["pos"] = [random.randint(0, window_size[0] - player_size), random.randint(0, window_size[1] - player_size)]

def main():
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Pygame Grid Game")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_input()
        move_enemies()

        screen.fill((0, 0, 0))
        draw_grid(screen)
        draw_walls(screen)
        draw_player(screen)
        draw_enemies(screen)
        draw_dots(screen)

        if not dots:
            show_winning_screen(screen)
            running = False

        pygame.display.flip()
        pygame.time.wait(30)

    pygame.quit()

if __name__ == "__main__":
    main()