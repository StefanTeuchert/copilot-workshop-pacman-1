import pygame
import math
import random

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
    {"pos": [300, 300], "color": (255, 0, 0)},  # Rot
    {"pos": [500, 300], "color": (0, 255, 0)},  # Grün
    {"pos": [700, 300], "color": (0, 0, 255)}   # Blau
]

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

def move_enemies():
    for enemy in enemies:
        direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        new_pos = [enemy["pos"][0] + direction[0] * 5, enemy["pos"][1] + direction[1] * 5]
        enemy_rect = pygame.Rect(new_pos[0], new_pos[1], player_size, player_size)
        if not any(enemy_rect.colliderect(wall) for wall in walls) and 0 <= new_pos[0] <= window_size[0] - player_size and 0 <= new_pos[1] <= window_size[1] - player_size:
            enemy["pos"] = new_pos

def handle_input():
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

    # Kollisionsabfrage mit Gegnern
    if any(player_rect.colliderect(pygame.Rect(enemy["pos"][0], enemy["pos"][1], player_size, player_size)) for enemy in enemies):
        reset_game()

def reset_game():
    global player_pos
    player_pos = [100, 100]
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

        pygame.display.flip()
        pygame.time.wait(30)

    pygame.quit()

if __name__ == "__main__":
    main()