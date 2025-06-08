import pygame
import random
from circleshape import CircleShape
from constants import *


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
        else:
            random_angle = random.uniform(20, 50)
            new_vector_left = self.velocity.rotate(-random_angle)
            new_vector_right = self.velocity.rotate(random_angle)
            new_raduis = self.radius - ASTEROID_MIN_RADIUS
            new_asteroid_left = Asteroid(self.position.x, self.position.y, new_raduis)
            new_asteroid_right = Asteroid(self.position.x, self.position.y, new_raduis)
            new_asteroid_left.velocity = new_vector_left * 1.2
            new_asteroid_right.velocity = new_vector_right *1.2