import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Window title
pygame.display.set_caption("Car Game")

# Colors
gray = (100, 100, 100)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
player_car_color = blue
enemy_car_colors = [red, green, white]

# Player car
car_surface = pygame.Surface((40, 60))
car_surface.fill(player_car_color)
car_rect = car_surface.get_rect()
car_rect.center = (screen_width // 2, screen_height - 100)
car_speed = 5

# Road lines
strip_surface = pygame.Surface((10, 80))
strip_surface.fill(yellow)
strips = []
for i in range(5):
    strip_rect = strip_surface.get_rect()
    strip_rect.center = (screen_width / 2, i * 150)
    strips.append(strip_rect)
strip_speed = 5

# Enemy cars
enemy_cars = []
for i in range(4):
    enemy_surface = pygame.Surface((40, 60))
    enemy_surface.fill(random.choice(enemy_car_colors))
    enemy_rect = enemy_surface.get_rect()
    enemy_rect.center = (random.randint(50, screen_width - 50), -i * 200)
    enemy_cars.append({"rect": enemy_rect, "surface": enemy_surface})
enemy_speed = 5

# Score
score = 0
font = pygame.font.SysFont(None, 55)

def start_screen():
    screen.fill(gray)
    start_text = font.render("Press any key to start", True, (255, 255, 255))
    text_rect = start_text.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(start_text, text_rect)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

# Game loop
start_screen()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_rect.x -= car_speed
    if keys[pygame.K_RIGHT]:
        car_rect.x += car_speed

    # Boundary checking
    if car_rect.left < 0:
        car_rect.left = 0
    if car_rect.right > screen_width:
        car_rect.right = screen_width

    # Fill the background
    screen.fill(gray)

    # Animate and draw strips
    for strip_rect in strips:
        strip_rect.y += strip_speed
        if strip_rect.top > screen_height:
            strip_rect.bottom = 0
        screen.blit(strip_surface, strip_rect)

    # Animate and draw enemy cars
    for enemy in enemy_cars:
        enemy["rect"].y += enemy_speed
        if enemy["rect"].top > screen_height:
            enemy["rect"].bottom = 0
            enemy["rect"].centerx = random.randint(50, screen_width - 50)
            enemy["surface"].fill(random.choice(enemy_car_colors))
        screen.blit(enemy["surface"], enemy["rect"])

        # Collision detection
        if car_rect.colliderect(enemy["rect"]):
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(screen_width/2, screen_height/2))
            screen.blit(game_over_text, text_rect)
            pygame.display.update()
            time.sleep(2)
            running = False

    # Draw the car
    screen.blit(car_surface, car_rect)

    # Update score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    score += 1

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
