import os

import pygame
import random
import sys

# Constants for the game setup
MIGRANT_GROUPS = ['African', 'Caribbean', 'North American']
TIME_PERIODS = {'Winter': 'hard', 'Summer': 'normal', 'Autumn': 'normal', 'Spring': 'easy'}
DESTINATIONS = ['Russia']
PLAYER_CLASSES = {
    'banker': {'funds': 4000, 'description': 'Starts with £4000'},
    'farmer': {'funds': 1200, 'description': 'Starts with £1200'},
    'student': {'funds': 700, 'description': 'Starts with £700'}
}

TRANSPORTATION = {'car': {'speed': 60, 'cost': 300}, 'road': {'speed': 40, 'cost': 100}, 'bike': {'speed': 20, 'cost': 50}}
SUPPLIES = {'food': 10, 'tires': 30, 'clothing': 20, 'water': 5}

# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 400, 300
FONT = pygame.font.SysFont(None, 24)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 180)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Edu Odyssey")

# Set panel size
panel_width = 800
panel_height = 600

# Load background image
background_image = pygame.image.load(os.path.join('landscape.png')).convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load retro style font
font = pygame.font.Font(None, 36)

# Function to display text
def draw_text(text_lines, font, color, surface, x, y):
    for i, line in enumerate(text_lines):
        text_obj = font.render(line, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y + i * 30)  # Adjust spacing between lines
        surface.blit(text_obj, text_rect)

# Function to display buttons
def draw_button(text, font, color, hover_color, surface, rect, callback=None):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, rect)
        if mouse_click[0] == 1 and callback:
            callback()
    else:
        pygame.draw.rect(surface, color, rect)

    draw_text([text], font, BLACK, surface, rect.x + 10, rect.y + 10)

# Game setup functions
def setup_game():
    print("Welcome to Edu Odyssey!\nPlease set up your journey.")

    group = get_user_choice("Choose your migrant group:", MIGRANT_GROUPS)
    period_key = get_user_choice("Choose the time period for your journey:", list(TIME_PERIODS.keys()))
    period = TIME_PERIODS[period_key]
    destination = get_user_choice("Choose your destination:", DESTINATIONS)
    player_class = get_user_choice("Choose your class:", list(PLAYER_CLASSES.keys()))
    team_names = pick_team_names(5)
    funds = PLAYER_CLASSES[player_class]['funds']
    transportation = get_user_choice("Choose your transportation:", list(TRANSPORTATION.keys()))
    speed = TRANSPORTATION[transportation]['speed']
    funds -= TRANSPORTATION[transportation]['cost']

    return {'group': group, 'period': period_key, 'destination': destination,
            'class': player_class, 'team_names': team_names, 'funds': funds,
            'distance': 1000, 'health': 100, 'difficulty': period, 'speed': speed}

# Function to get user choice using Pygame interface
def get_user_choice(prompt, options):
    choice = None
    while choice is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, option in enumerate(options):
                    rect = pygame.Rect(50, 50 + i * 50, 200, 40)
                    if rect.collidepoint(event.pos):
                        choice = option
        SCREEN.fill(BLACK)
        draw_text([prompt], FONT, WHITE, SCREEN, 10, 10)  # Draw prompt
        for i, option in enumerate(options):
            rect = pygame.Rect(100, 80 + i * 50, 200, 40)
            draw_button(option, FONT, BLUE, GRAY, SCREEN, rect)
        pygame.display.flip()
    return choice

# Game functions (remaining functions remain the same)
def pick_team_names(num_members):
    team_names = []
    for i in range(num_members):
        name = input(f"Enter name for member {i + 1}: ")
        team_names.append(name)
    return team_names

def get_random_event(difficulty):
    base_events = ['Find Food', 'Lose Money', 'Gain Money', 'Illness', 'None', 'Buy Supplies']
    if difficulty == 'hard':
        base_events += ['Robbery', 'Severe Weather']
    elif difficulty == 'easy':
        base_events += ['Bountiful Harvest', 'Found Treasure']
    return random.choice(base_events)

def process_event(event, game_state):
    if event == 'Find Food':
        print("You found food! Health increases.")
        game_state['health'] += 10
    elif event == 'Lose Money':
        print("You lost some money.")
        game_state['funds'] -= 50
    elif event == 'Gain Money':
        print("You found some money!")
        game_state['funds'] += 50
    elif event == 'Illness':
        print("A team member is ill. Health decreases.")
        game_state['health'] -= 20
    elif event == 'Buy Supplies':
        print("You bought supplies.")
        game_state['funds'] -= 100

def player_decision(game_state):
    decision = get_user_choice("Choose an action:", ['Rest', 'Hunt', 'Buy Supplies', 'Continue'])
    if decision == 'Rest':
        print("Resting... Health improves.")
        game_state['health'] += 15
        game_state['health'] = min(game_state['health'], 100)
    elif decision == 'Hunt':
        print("Hunting for food...")
        game_state['health'] += random.randint(5, 10)
        game_state['health'] = min(game_state['health'], 100)
    elif decision == 'Buy Supplies':
        buy_supplies(game_state)
    elif decision == 'Continue':
        game_state['health'] -= random.randint(7, 15)
        game_state['health'] = min(game_state['health'], 100)

def check_endgame_conditions(game_state):
    if game_state['distance'] <= 0:
        return 'win'
    elif game_state['health'] <= 0 or game_state['funds'] <= 0:
        return 'lose'
    return 'continue'

def main_game_loop(game_state):
    while True:
        player_decision(game_state)

        if random.random() < 0.1:
            major_obstacle(game_state)

        event = get_random_event(game_state['difficulty'])
        process_event(event, game_state)

        game_state['distance'] -= game_state['speed']
        print(f"Remaining distance: {game_state['distance']}, Health: {game_state['health']}, Funds: {game_state['funds']}")
        draw_text([f"Remaining distance: {game_state['distance']}", f"Health: {game_state['health']}", f"Funds: {game_state['funds']}"], FONT, BLACK, SCREEN, 10, 300)

        status = check_endgame_conditions(game_state)
        if status != 'continue':
            return status

def buy_supplies(game_state):
    if game_state['funds'] > min(SUPPLIES.values()):
        supply = get_user_choice("Choose a supply to buy:", list(SUPPLIES.keys()))
        if game_state['funds'] >= SUPPLIES[supply]:
            game_state['funds'] -= SUPPLIES[supply]
            print(f"You bought {supply}.")
            if supply == 'food':
                game_state['health'] += 20
                game_state['health'] = min(game_state['health'], 100)
        else:
            print("Not enough funds to buy this supply.")
    else:
        print("You don't have enough funds to buy supplies.")

def major_obstacle(game_state):
    obstacle_type = random.choice(['Robbery', 'Disease'])
    if obstacle_type == 'Robbery':
        print("A robbery attack has occurred! You've lost funds and some health.")
        game_state['funds'] -= 100
        game_state['health'] -= 15
    elif obstacle_type == 'Disease':
        print("A disease outbreak has struck your team! Health significantly decreases.")
        game_state['health'] -= 35

# Initialize the game state and start the main game loop
game_state = setup_game()
game_status = main_game_loop(game_state)

if game_status == 'win':
    print("Congratulations! You've reached your destination and won the game!")
else:
    print("Unfortunately, your journey has ended in failure.")
