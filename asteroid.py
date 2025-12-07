import random
import pygame
import os
class Asteroid: 
    def __init__(self, grid_size, occupied_positions, existing_data=None):
        self.grid_size = grid_size
        self.sprite = None

        if existing_data:
            self.load_from_dict(existing_data)
        else:
            self.create_new_asteroid(occupied_positions)
        
        self.load_sprite()
    def create_new_asteroid(self, occupied_positions):
        """ Spawns an asteroid at a random edge """
        edge = random.randint(0, 3)
        #Top
        if edge == 0:
            self.x = random.randint(0, self.grid_size - 1)
            self.y = 0
            self.dx = random.choice([- 1, 0, 1])
            self.dy = 1 
        #Bottom
        elif edge == 1:
            self.x = random.randint(0, self.grid_size - 1)
            self.y = self.grid_size - 1
            self.dx = random.choice([- 1, 0, 1])
            self.dy = -1
        #left
        elif edge == 2:
            self.x = 0
            self.y = random.randint(0, self.grid_size - 1)
            self.dx = 1
            self.dy = random.choice([- 1, 0, 1])
        #right
        else:
            self.x = self.grid_size - 1
            self.y = random.randint(0, self.grid_size - 1)
            self.dx = -1
            self.dy = random.choice([- 1, 0, 1])
        #correction    
        if self.dx == 0 and self.dy == 0:
            self.dx, self.dy = 1, 1
        #correction for station and player
        if (self.x, self.y) in occupied_positions:
            self.create_new_asteroid(occupied_positions)
    def load_sprite(self):
        """Attempts to load sprite"""
        try: 
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sprite_path = os.path.join(current_dir, 'sprites', 'Asteroid.png')
            loaded_sprite = pygame.image.load(sprite_path)
            self.sprite = pygame.transform.scale(loaded_sprite, (32, 32))
        except (pygame.error, FileNotFoundError):
            self.sprite = None
    def move(self, avoid_locations=None):
        """Updates position, but waits if the next spot is blocked."""
        if avoid_locations is None:
            avoid_locations = set()

        next_x = self.x + self.dx
        next_y = self.y + self.dy
        
        # Only move if the space is empty
        if (next_x, next_y) in avoid_locations:
            hit_x_wall = (self.x + self.dx, self.y) in avoid_locations
            hit_y_wall = (self.x, self.y + self.dy) in avoid_locations
            if hit_x_wall:
                self.dx *= -1
                if self.dy == 0:
                    self.dy = random.choice([-1, 1])
            if hit_y_wall:
                self.dy *= -1
                if self.dx == 0:
                    self.dx = random.choice([-1, 1])
            #Corner Bounce
            if not hit_x_wall and not hit_y_wall:
                self.dx *= -1
                self.dy *= -1    
                next_x = self.x + self.dx
                next_y = self.y + self.dy
            
        if (next_x, next_y) not in avoid_locations:
            self.x = next_x
            self.y = next_y
    def is_out_of_bounds(self):
        """The asteroid has left the building"""
        return not (0 <= self.x < self.grid_size and 0 <= self.y < self.grid_size)
    def get_pos(self):
        return (self.x, self.y)
    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'dx': self.dx,
            'dy': self.dy
        }
    def load_from_dict(self, data):
        self.x = data['x']
        self.y = data['y']
        self.dx = data['dx']
        self.dy = data['dy']