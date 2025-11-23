import random

#colors
COLOR_RED = (200, 0, 0)
COLOR_GREEN = (0, 200, 0)
COLOR_BLUE = (0, 0, 200)
COLOR_YELLOW = (200, 200, 0)

class WanderingMonster:
    def __init__(self,grid_size, town_pos, existing_data=None):
        """
        Initialize a monster,
        Load existing_data from save,
        or generate new random monster
        """
        self.grid_size = grid_size
        if existing_data:
            self.load_from_dict(existing_data)
        else:
            self.create_new_random_monster(town_pos)
    def create_new_random_monster(self, town_pos):
        """
        Creates a monster with randomized stats and a unique position.
        """
        monster_types = [
            {'name': 'Goblin',
             'description': 'A Goblin who looks unhappy you are here',
             'health_range': (20, 40),
             'power_range': (8, 12),
             'money_range': (10, 30),
             'color': COLOR_RED},
            {'name': 'Slime',
             'description': 'A gelatinous green blob.',
             'health_range': (10, 20),
             'power_range': (4, 8),
             'money_range': (5, 15),
             'color': COLOR_GREEN},
            {'name': 'Vulture',
             'description': 'A smelly angry bird',
             'health_range': (15, 35),
             'power_range': (6, 10),
             'money_range': (15, 25),
             'color': COLOR_YELLOW},
            {'name': 'Troll',
             'description': 'A large creature with a giant club.',
             'health_range': (50, 80),
             'power_range': (20, 30),
             'money_range': (50, 100),
             'color': COLOR_BLUE}
        ]

        data = random.choice(monster_types)
        
        self.name = data['name']
        self.description = data['description']
        self.health = random.randint(*data['health_range'])
        self.max_health = self.health
        self.power = random.randint(*data['power_range'])
        self.money = int(random.randint(*data['money_range']) * (random.random() * 0.2 + 0.9))
        self.color = data['color']
        
        # Generate Position besides town
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) != town_pos:
                self.x = x
                self.y = y
                break 
    def move(self, town_pos, turn_count):
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
            'y': self.y
        }
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