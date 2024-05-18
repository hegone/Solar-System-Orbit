import pygame
import math

# Initialize Pygame
pygame.init()

# Define screen dimensions
screen_width, screen_height = 1200, 800
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Solar System Simulation")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARKGRAY = (105, 105, 105)

# Define planets
planets = [
    {'name': 'Mercury', 'radius': 0.39, 'period': 0.24, 'size': 3, 'color': GRAY},
    {'name': 'Venus', 'radius': 0.72, 'period': 0.62, 'size': 5, 'color': (255, 255, 0)},
    {'name': 'Earth', 'radius': 1.00, 'period': 1.00, 'size': 5, 'color': BLUE},
    {'name': 'Mars', 'radius': 1.52, 'period': 1.88, 'size': 4, 'color': RED},
    {'name': 'Jupiter', 'radius': 5.20, 'period': 11.86, 'size': 11, 'color': (255, 165, 0)},
    {'name': 'Saturn', 'radius': 9.58, 'period': 29.46, 'size': 9, 'color': (218, 165, 32)},
    {'name': 'Uranus', 'radius': 19.22, 'period': 84.01, 'size': 8, 'color': (173, 216, 230)},
    {'name': 'Neptune', 'radius': 30.05, 'period': 164.79, 'size': 8, 'color': (0, 0, 255)},
]

# Center of the screen
center_x = screen_width // 2
center_y = screen_height // 2

# Simulation parameters
scale = 10  # Initial scale for the orbital distances, set to capture the entire solar system
default_scale = scale
speed = 1  # Speed multiplier for the simulation
default_speed = speed
day = 0
running_simulation = True  # Controls the play/pause state

# Initialize mouse drag and speed adjustment positions
mouse_drag = None
adjusting_speed = False

# Font for displaying text
font = pygame.font.Font(None, 24)

# Function to draw orbits
def draw_orbits():
    for planet in planets:
        radius = planet['radius'] * scale
        pygame.draw.circle(screen, WHITE, (center_x, center_y), int(radius), 1)

# Function to draw planets
def draw_planets(day):
    for planet in planets:
        angle = 2 * math.pi * (day / (planet['period'] * 365))
        x = int(center_x + planet['radius'] * scale * math.cos(angle))
        y = int(center_y + planet['radius'] * scale * math.sin(angle))
        pygame.draw.circle(screen, planet['color'], (x, y), planet['size'])
        planet['pos'] = (x, y)

# Function to display info on hover
def display_info(mouse_pos):
    for planet in planets:
        if math.hypot(planet['pos'][0] - mouse_pos[0], planet['pos'][1] - mouse_pos[1]) <= planet['size']:
            info = f"{planet['name']}: Radius={planet['radius']} AU, Period={planet['period']} years"
            text = font.render(info, True, WHITE)
            screen.blit(text, (mouse_pos[0] + 10, mouse_pos[1] - 10))

# Function to draw the play/pause button
def draw_button():
    button_text = "Pause" if running_simulation else "Play"
    button_color = RED if running_simulation else GREEN
    button = pygame.Rect(10, 10, 80, 30)
    pygame.draw.rect(screen, button_color, button)
    text = font.render(button_text, True, BLACK)
    screen.blit(text, (button.x + 10, button.y + 5))
    return button

# Function to draw the speed control bar
def draw_speed_control():
    bar = pygame.Rect(100, 10, 200, 30)
    pygame.draw.rect(screen, DARKGRAY, bar)
    handle_position = int(100 + (speed - 0.1) * 18)
    handle = pygame.Rect(handle_position, 10, 20, 30)
    pygame.draw.rect(screen, WHITE, handle)
    return bar, handle

# Function to draw the reset button
def draw_reset_button():
    button = pygame.Rect(320, 10, 80, 30)
    pygame.draw.rect(screen, GREEN, button)
    text = font.render("Reset", True, BLACK)
    screen.blit(text, (button.x + 10, button.y + 5))
    return button

# Function to draw the current speed display
def draw_current_speed():
    text = font.render(f"Speed: {speed:.1f}x", True, WHITE)
    screen.blit(text, (410, 15))

# Main loop
running = True
clock = pygame.time.Clock()
fullscreen = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:  # Zoom in
                scale *= 1.1
            elif event.key == pygame.K_MINUS:  # Zoom out
                scale /= 1.1
            elif event.key == pygame.K_f:  # Toggle fullscreen
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_drag = event.pos
                if draw_button().collidepoint(event.pos):
                    running_simulation = not running_simulation
                if draw_reset_button().collidepoint(event.pos):
                    speed = default_speed
                    scale = default_scale
                bar, handle = draw_speed_control()
                if handle.collidepoint(event.pos):
                    adjusting_speed = True
                else:
                    adjusting_speed = False
            elif event.button == 4:  # Scroll up
                scale *= 1.1
            elif event.button == 5:  # Scroll down
                scale /= 1.1
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                mouse_drag = None
                adjusting_speed = False
        elif event.type == pygame.MOUSEMOTION:
            if adjusting_speed:
                new_speed = (event.pos[0] - 100) / 18 + 0.1
                speed = max(0.1, min(new_speed, 10))  # Speed range from 0.1 to 10
            elif mouse_drag:
                dx, dy = event.rel
                center_x += dx
                center_y += dy

    screen.fill(BLACK)
    pygame.draw.circle(screen, YELLOW, (center_x, center_y), 10)
    draw_orbits()
    draw_planets(day)
    display_info(pygame.mouse.get_pos())
    draw_button()
    draw_speed_control()
    draw_reset_button()
    draw_current_speed()
    
    if running_simulation:
        day += speed
    clock.tick(60)  # 60 frames per second
    pygame.display.flip()

pygame.quit()
