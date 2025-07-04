import pygame
from game_objects.circleshape import CircleShape
from config.constants import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS) 
    
    def draw(self, screen):
        pygame.draw.circle(screen, "orange", self.position, self.radius, 2)
        
    def update(self, dt):
        self.position += self.velocity * dt