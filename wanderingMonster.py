import random
import pygame
import os
#colors
COLOR_RED = (200, 0, 0)
COLOR_GREEN = (0, 200, 0)
COLOR_BLUE = (0, 0, 200)
COLOR_PURPLE = (100, 0, 100)

class WanderingMonster:
    def __init__(self,grid_size, town_pos, existing_data=None):
        """
        Initialize a monster,
        Load existing_data from save,
        or generate new random monster
        """
        self.grid_size = grid_size
        self.sprite = None
        if existing_data:
            self.load_from_dict(existing_data)
        else:
            self.create_new_random_monster(town_pos)
        self.load_sprite()
    def load_sprite(self):
        """
        Attempts to load sprite for monster
        Will revert to old circles if loading fails
        """
        target_sprite = getattr(self, 'sprite_name', None)
        
        if target_sprite:
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                sprite_path = os.path.join(current_dir, 'sprites', target_sprite)
                loaded_sprite = pygame.image.load(sprite_path)
                self.sprite = pygame.transform.scale(loaded_sprite, (32, 32))
            except (pygame.error, FileNotFoundError) as e:
                print(f"Warning: Failed to load '{target_sprite}'")
                print(f"   --> Attempted path: {sprite_path}")
                print(f"   --> Error: {e}")
                self.sprite = None
                
    def create_new_random_monster(self, town_pos):
        """
        Creates a monster with randomized stats and a unique position.
        """
        monster_types = [
            {'name': 'Martian',
             'description': 'A ship approaches from the planet Mars. They attack you, because Martians do that.',
             'health_range': (15, 30),
             'power_range': (8, 12),
             'money_range': (10, 30),
             'color': COLOR_RED,
             'sprite':'BadShipR.png',
             'crit_chance': 0.15, 
             'crit_multiplier': 1.5, 
             'miss_chance': 0.10},
            {'name': 'Cyborg',
             'description': 'A cyborg vessel. They would love to give you new features.',
             'health_range': (5, 15),
             'power_range': (15, 20),
             'money_range': (5, 15),
             'color': COLOR_GREEN,
             'sprite':'BadShipG.png',
             'crit_chance': 0.10, 
             'crit_multiplier': 1.5, 
             'miss_chance': 0.05},
            {'name': 'Space Pirate',
             'description': 'This ship seems like it might be hiding something. Hopefully credits.',
             'health_range': (15, 35),
             'power_range': (6, 7),
             'money_range': (15, 50),
             'color': COLOR_PURPLE,
             'sprite':'BadShipP.png',
             'crit_chance': 0.10, 
             'crit_multiplier': 2.0, 
             'miss_chance': 0.25},
            {'name': '???',
             'description': 'Something here is not right, is it time to flee?',
             'health_range': (30, 45),
             'power_range': (25, 30),
             'money_range': (50, 100),
             'color': COLOR_BLUE,
             'sprite':'BadShipB.png',
             'crit_chance': 0.10, 
             'crit_multiplier': 2.0, 
             'miss_chance': 0.00
             }
             ]

        data = random.choice(monster_types)
        
        self.name = data['name']
        self.description = data['description']
        self.health = random.randint(*data['health_range'])
        self.max_health = self.health
        self.power = random.randint(*data['power_range'])
        self.money = int(random.randint(*data['money_range']) * (random.random() * 0.2 + 0.9))
        self.color = data['color']
        self.sprite_name = data['sprite']
        self.crit_chance = data.get('crit_chance', 0.05)
        self.crit_multiplier = data.get('crit_multiplier', 1.5)
        self.miss_chance = data.get('miss_chance', 0.05)   
        
        # Generate Position besides town
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) != town_pos:
                self.x = x
                self.y = y
                break 
    def move(self, town_pos, turn_count, obstacles=None):
        """
        Attempts to move the monster in a random direction.
        Will not move off grid or into town.
        Moves every other turn, with a 25% chance of moving 2 squares.
        """
        if turn_count % 2 == 0:
            return # Skip move this turn

        # Determine move distance
        move_distance = 1
        if random.random() < 0.25: 
            move_distance = 2
        #Obstacle
        if obstacles is None:
            obstacles = set()
        else:
            obstacles = set(obstacles)
        directions = [
            (0, -1), # Up
            (0, 1),  # Down
            (-1, 0), # Left
            (1, 0),   # Right
            (1,1),    #NW
            (1,-1),   #NE
            (-1,1),   #SW
            (-1,-1)   #SE
        ]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x = self.x + dx * move_distance
            new_y = self.y + dy * move_distance

            # Check boundaries
            if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                # Check town collision
                if (new_x, new_y) != town_pos:
                    self.x = new_x
                    self.y = new_y
                    return # Move successful, stop trying directions

    def get_pos(self):
        return (self.x, self.y)

    def to_dict(self):
        """Puts monster in dictionary for saving."""
        return {
            'name': self.name,
            'description': self.description,
            'health': self.health,
            'max_health': self.max_health,
            'power': self.power,
            'money': self.money,
            'color': self.color,
            'x': self.x,
            'y': self.y,
            'sprite_name': getattr(self, 'sprite_name', None),
            'crit_chance': getattr(self, 'crit_chance', 0.05),
            'crit_multiplier': getattr(self, 'crit_multiplier', 1.5),
            'miss_chance': getattr(self, 'miss_chance', 0.05)}
    def load_from_dict(self, data):
        """Loads monster stats from a dictionary."""
        self.name = data['name']
        self.description = data['description']
        self.health = data['health']
        self.max_health = data.get('max_health', data['health'])
        self.power = data['power']
        self.money = data['money']
        self.color = tuple(data['color']) 
        self.x = data['x']
        self.y = data['y']
        self.sprite_name = data.get('sprite_name')
        self.crit_chance = data.get('crit_chance', 0.05)
        self.crit_multiplier = data.get('crit_multiplier', 1.5)
        self.miss_chance = data.get('miss_chance', 0.05)