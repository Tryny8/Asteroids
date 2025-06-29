import pygame
from config.constants import *
from entities.player import Player
from entities.asteroid import Asteroid
from entities.asteroid_manager import AsteroidField
from entities.shots import Shot
import asyncio

__version__ = '1.1.1'
"""
python tools/version_commit.py "Commit"
"""

async def main():
   print(f"Starting Asteroids! \n Screen width / height: {SCREEN_WIDTH} / {SCREEN_HEIGHT}")
   # Init window
   pygame.init()
   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
   clock = pygame.time.Clock()

   # Init Group
   updatable = pygame.sprite.Group()
   drawable = pygame.sprite.Group()
   asteroids = pygame.sprite.Group()
   shots = pygame.sprite.Group()
   
   Asteroid.containers = (asteroids, updatable, drawable)
   AsteroidField.containers = updatable
   Player.containers = (updatable, drawable)
   Shot.containers = (shots, updatable, drawable)

   # Init Object
   asteroidField = AsteroidField()
   
   player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
   
   # Init Text in Game
   police = pygame.font.Font("font/Arial.ttf", 50)
   police_data = pygame.font.Font("font/Arial.ttf", 25)
   # police = pygame.font.SysFont("monospace", 50)
   text_version = police_data.render (f"Version: {__version__}", 2, "green")
   text_Gui = police_data.render ("Gui - Standby", 2, "green")
   text_end_game = police.render ("Game over!", 2, "red")
   text_shoot = police.render ("Touché", 2, "red")

   # Loop Game   
   dt = 0
   running = True
   while running:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            return
      
      # Update Ecran
      screen.fill("black")
      
      # Update object
      updatable.update(dt)
      screen.blit(text_version, (10, 0))
      screen.blit(text_Gui, ((SCREEN_WIDTH / 2) - 80, 0))
      
      # Draw object
      for obj in drawable:
         obj.draw(screen)
         
      for asteroid in asteroids:
         if asteroid.check_colliding(player):
            screen.blit(text_end_game, ((SCREEN_WIDTH / 2) - 133, (SCREEN_HEIGHT / 2) - 30))
            running = False
         for shot in shots:
            if asteroid.check_colliding(shot):
               screen.blit(text_shoot, ((SCREEN_WIDTH / 2) - 133, (SCREEN_HEIGHT / 2) - 30))
               shot.kill()
               asteroid.split() 
      
      pygame.display.flip()
      
      # limit the framerate to 60 FPS
      dt = clock.tick(60) / 1000
      await asyncio.sleep(0)
   
   # Quit programme
   pygame.time.wait(3000)
   pygame.quit()


asyncio.run(main())