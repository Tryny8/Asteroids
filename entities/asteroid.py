import pygame
import random
from game_objects.circleshape import CircleShape
from config.constants import *


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)    
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        
    def update(self, dt):
        self.position += self.velocity * dt
    
    def split(self):
        self.kill()
        
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        # randomize the angle of the split
        random_angle = random.uniform(20, 50)
        
        vect_left = self.velocity.rotate(-random_angle)
        vect_right = self.velocity.rotate(random_angle)
        
        raduis = self.radius - ASTEROID_MIN_RADIUS
        
        asteroid_left = Asteroid(self.position.x, self.position.y, raduis)
        asteroid_left.velocity = vect_left * 1.2
        
        asteroid_right = Asteroid(self.position.x, self.position.y, raduis)
        asteroid_right.velocity = vect_right *1.2