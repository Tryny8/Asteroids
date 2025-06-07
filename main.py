import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField


def main():
   print(f"Starting Asteroids! \n Screen width / height: {SCREEN_WIDTH} / {SCREEN_HEIGHT}")
   
   # Init window
   pygame.init()
   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
   clock = pygame.time.Clock()
   
   # Init Group
   updatable = pygame.sprite.Group()
   drawable = pygame.sprite.Group()
   asteroids = pygame.sprite.Group()
   
   Asteroid.containers = (asteroids, updatable, drawable)
   AsteroidField.containers = updatable
   Player.containers = (updatable, drawable)

   # Init Object
   asteroidField = AsteroidField()
   player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

   # Loop Game   
   dt = 0
   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            return
      
      # Update Ecran
      screen.fill("black")
      
      # Update and draw object
      updatable.update(dt)
      
      for obj in drawable:
         obj.draw(screen)
            
      pygame.display.flip()
      
      # limit the framerate to 60 FPS
      dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()