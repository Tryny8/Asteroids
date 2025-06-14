import pygame
from game_objects.circleshape import CircleShape
from config.config import *
from config.constants import *
from entities.shots import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self):
        if self.shoot_timer > 0:
            return 
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        
    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[KEY_LEFT]:
            # Key left
            self.rotate(-dt)
        if keys[KEY_RIGHT]:
            # Key right
            self.rotate(dt)
        if keys[KEY_UP]:
            # Key forward
            self.move(dt)
        if keys[KEY_DOWN]:
            # Key backward
            self.move(-dt)
        if keys[KEY_SHOOT]:
            # Key Space (Shoot)
            self.shoot()