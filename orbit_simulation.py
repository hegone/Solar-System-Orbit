import pygame
import math

# Initialize Pygame
pygame.init()

# Load custom font
font_path = 'Solar-System-Orbit/Pretendard-Medium.otf'
font = pygame.font.Font(font_path, 24)

# Define initial screen dimensions
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

# Define the Sun
sun = {
    'name': 'Sun',
    'size': 20,  # Fixed size for display
    'color': YELLOW,
    'circumference': '4,379,000 km',
    'mass': '1.989 × 10³⁰ kg',
    'distance_from_earth': '147 million km'
}

# Define planets with realistic semi-major axis (in astronomical units), period (in Earth years),
# size (radius in km), and additional information.
planets = [
    {'name': 'Mercury', 'radius': 0.39, 'period': 0.24, 'size': 2440, 'color': GRAY,
     'circumference': '15,329 km', 'mass': '3.30 × 10²³ kg', 'distance_from_earth': '77 million km'},
    {'name': 'Venus', 'radius': 0.72, 'period': 0.62, 'size': 6052, 'color': (255, 255, 0),
     'circumference': '38,025 km', 'mass': '4.87 × 10²⁴ kg', 'distance_from_earth': '41 million km'},
    {'name': 'Earth', 'radius': 1.00, 'period': 1.00, 'size': 6371, 'color': BLUE,
     'circumference': '40,075 km', 'mass': '5.97 × 10²⁴ kg', 'distance_from_earth': '0 km'},
    {'name': 'Mars', 'radius': 1.52, 'period': 1.88, 'size': 3390, 'color': RED,
     'circumference': '21,344 km', 'mass': '6.42 × 10²³ kg', 'distance_from_earth': '78 million km'},
    {'name': 'Jupiter', 'radius': 5.20, 'period': 11.86, 'size': 69911, 'color': (255, 165, 0),
     'circumference': '439,264 km', 'mass': '1.90 × 10²⁷ kg', 'distance_from_earth': '628 million km'},
    {'name': 'Saturn', 'radius': 9.58, 'period': 29.46, 'size': 58232, 'color': (218, 165, 32),
     'circumference': '378,675 km', 'mass': '5.68 × 10²⁶ kg', 'distance_from_earth': '1.2 billion km'},
    {'name': 'Uranus', 'radius': 19.22, 'period': 84.01, 'size': 25362, 'color': (173, 216, 230),
     'circumference': '160,590 km', 'mass': '8.68 × 10²⁵ kg', 'distance_from_earth': '2.6 billion km'},
    {'name': 'Neptune', 'radius': 30.05, 'period': 164.79, 'size': 24622, 'color': (0, 0, 255),
     'circumference': '155,600 km', 'mass': '1.02 × 10²⁶ kg', 'distance_from_earth': '4.3 billion km'},
]

# Center of the screen
center_x = screen_width // 2
center_y = screen_height // 2

# Simulation parameters
scale = 25  # Initial scale for the orbital distances, set to capture the entire solar system
default_scale = scale
speed = 1  # Speed multiplier for the simulation
default_speed = speed
day = 0
running_simulation = True  # Controls the play/pause state
show_controls = True  # Controls the visibility of play/pause and speed control
focused_planet = None  # Planet being followed

# Initialize mouse drag and speed adjustment positions
mouse_drag = None
adjusting_speed = False
dragging_handle = False

# Accelerate/Decelerate control variables
acceleration = 0.01
speed_change = 0

# Function to draw orbits
def draw_orbits():
    for planet in planets:
        radius = planet['radius'] * scale
        pygame.draw.circle(screen, WHITE, (center_x, center_y), int(radius), 1)

# Function to draw planets
def draw_planets(day):
    global center_x, center_y
    for planet in planets:
        angle = 2 * math.pi * (day / (planet['period'] * 365))
        x = int(center_x + planet['radius'] * scale * math.cos(angle))
        y = int(center_y + planet['radius'] * scale * math.sin(angle))
        size = max(1, int(planet['size'] * scale / 1e5))  # Adjust size relative to zoom
        pygame.draw.circle(screen, planet['color'], (x, y), size)
        planet['pos'] = (x, y)
        if focused_planet == planet:
            # Center the view on the focused planet
            center_x = screen_width // 2 - int(planet['radius'] * scale * math.cos(angle))
            center_y = screen_height // 2 - int(planet['radius'] * scale * math.sin(angle))

# Function to display info on hover
def display_info(mouse_pos):
    # Check for Sun first
    sun_size = sun['size']
    if math.hypot(center_x - mouse_pos[0], center_y - mouse_pos[1]) <= sun_size:
        info = [
            f"Name: {sun['name']}",
            f"Circumference: {sun['circumference']}",
            f"Mass: {sun['mass']}",
            f"Distance from Earth: {sun['distance_from_earth']}"
        ]
        for i, line in enumerate(info):
            text = font.render(line, True, WHITE)
            screen.blit(text, (mouse_pos[0] + 10, mouse_pos[1] - 10 + i * 20))
        return  # Only show Sun info

    # Check for planets
    for planet in planets:
        size = max(1, int(planet['size'] * scale / 1e5))
        if math.hypot(planet['pos'][0] - mouse_pos[0], planet['pos'][1] - mouse_pos[1]) <= size:
            info = [
                f"Name: {planet['name']}",
                f"Radius: {planet['radius']} AU",
                f"Period: {planet['period']} years",
                f"Circumference: {planet['circumference']}",
                f"Mass: {planet['mass']}",
                f"Distance from Earth: {planet['distance_from_earth']}"
            ]
            for i, line in enumerate(info):
                text = font.render(line, True, WHITE)
                screen.blit(text, (mouse_pos[0] + 10, mouse_pos[1] - 10 + i * 20))
            break  # Display only one info box

# Function to draw the play/pause button
def draw_button():
    button_text = "Pause" if running_simulation else "Play"
    button_color = RED if running_simulation else GREEN
    button = pygame.Rect(10, 50, 80, 30)
    pygame.draw.rect(screen, button_color, button)
    text = font.render(button_text, True, BLACK)
    screen.blit(text, (button.x + 10, button.y + 5))
    return button

# Function to draw the speed control bar
def draw_speed_control():
    bar = pygame.Rect(10, 90, 200, 30)
    pygame.draw.rect(screen, DARKGRAY, bar)
    handle_position = int(10 + (speed - 0.1) * 18)
    handle = pygame.Rect(handle_position, 90, 20, 30)
    pygame.draw.rect(screen, WHITE, handle)
    return bar, handle

# Function to draw the reset button
def draw_reset_button():
    button = pygame.Rect(10, 170, 80, 30)
    pygame.draw.rect(screen, GREEN, button)
    text = font.render("Reset", True, BLACK)
    screen.blit(text, (button.x + 10, button.y + 5))
    return button

# Function to draw the menu button
def draw_menu_button():
    button = pygame.Rect(10, 10, 80, 30)
    pygame.draw.rect(screen, BLUE, button)
    text = font.render("Menu", True, BLACK)
    screen.blit(text, (button.x + 10, button.y + 5))
    return button

# Function to draw planet buttons
def draw_planet_buttons():
    buttons = []
    for i, planet in enumerate(planets):
        button = pygame.Rect(10, 210 + i * 40, 150, 30)
        pygame.draw.rect(screen, planet['color'], button)
        text = font.render(planet['name'], True, BLACK)
        screen.blit(text, (button.x + 10, button.y + 5))
        buttons.append((button, planet))
    return buttons

# Function to draw current speed
def draw_current_speed():
    speed_text = f"Speed: {speed:.1f}x"
    text = font.render(speed_text, True, WHITE)
    screen.blit(text, (10, 130))

# Function to focus on a planet
def focus_on_planet(planet):
    global center_x, center_y, scale, focused_planet
    scale = 400 / planet['radius']  # Adjust scale to focus on the planet
    focused_planet = planet  # Set the planet to be followed

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:  # Zoom in
                scale *= 1.1
            elif event.key == pygame.K_MINUS:  # Zoom out
                scale /= 1.1
            elif event.key == pygame.K_SPACE:  # Play/pause toggle
                running_simulation = not running_simulation
            elif event.key == pygame.K_RIGHT:  # Increase speed
                speed_change = acceleration
            elif event.key == pygame.K_LEFT:  # Decrease speed
                speed_change = -acceleration
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                speed_change = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_drag = event.pos
                if draw_menu_button().collidepoint(event.pos):
                    show_controls = not show_controls
                if show_controls:
                    if draw_button().collidepoint(event.pos):
                        running_simulation = not running_simulation
                    if draw_reset_button().collidepoint(event.pos):
                        speed = default_speed
                        scale = default_scale
                        focused_planet = None  # Reset focus
                    bar, handle = draw_speed_control()
                    if handle.collidepoint(event.pos):
                        dragging_handle = True
                    if bar.collidepoint(event.pos) and not dragging_handle:
                        new_speed = (event.pos[0] - 10) / 18 + 0.1
                        speed = max(0.1, min(new_speed, 10))  # Speed range from 0.1 to 10
                    planet_buttons = draw_planet_buttons()
                    for button, planet in planet_buttons:
                        if button.collidepoint(event.pos):
                            focus_on_planet(planet)
            elif event.button == 4:  # Scroll up
                mouse_x, mouse_y = event.pos
                scale *= 1.1
                center_x = (center_x - mouse_x) * 1.1 + mouse_x
                center_y = (center_y - mouse_y) * 1.1 + mouse_y
            elif event.button == 5:  # Scroll down
                mouse_x, mouse_y = event.pos
                scale /= 1.1
                center_x = (center_x - mouse_x) / 1.1 + mouse_x
                center_y = (center_y - mouse_y) / 1.1 + mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_drag = None
                dragging_handle = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_drag:
                if not dragging_handle:
                    dx, dy = event.pos[0] - mouse_drag[0], event.pos[1] - mouse_drag[1]
                    center_x += dx
                    center_y += dy
                    mouse_drag = event.pos
            elif dragging_handle:
                bar, handle = draw_speed_control()
                new_speed = (event.pos[0] - 10) / 18 + 0.1
                speed = max(0.1, min(new_speed, 10))  # Speed range from 0.1 to 10

    screen.fill(BLACK)

    # Draw the Sun
    sun_size = sun['size']  # Fixed size
    pygame.draw.circle(screen, sun['color'], (center_x, center_y), sun_size)

    # Update speed based on arrow key hold
    speed += speed_change

    # Update day based on the running simulation
    if running_simulation:
        day += speed

    draw_orbits()
    draw_planets(day)

    # Draw UI elements
    menu_button = draw_menu_button()
    if show_controls:
        play_pause_button = draw_button()
        speed_bar, speed_handle = draw_speed_control()
        reset_button = draw_reset_button()
        planet_buttons = draw_planet_buttons()
        draw_current_speed()

    # Display planet info on hover
    mouse_pos = pygame.mouse.get_pos()
    display_info(mouse_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
