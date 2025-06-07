import pygame
from constants import *
from player import Player


def main():
   # Init window
   pygame.init()
   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
   print("Starting Asteroids!")
   print(f"Screen width: {SCREEN_WIDTH}")
   print(f"Screen height: {SCREEN_HEIGHT}")
   
   # Init FPS
   clock = pygame.time.Clock()
   dt = 0
   
   # Init Group
   updatable = pygame.sprite.Group()
   drawable = pygame.sprite.Group()
   Player.containers = (updatable, drawable)
   
   # Init Player
   x = SCREEN_WIDTH / 2
   y = SCREEN_HEIGHT / 2
   player = Player(x, y)
   
   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            return
      
      # Update Ecran
      screen.fill("black")
      
      # Update Player
      updatable.update(dt)
      for sprite in drawable:
         sprite.draw(screen)
            
      pygame.display.flip()
      
      # limit the framerate to 60 FPS
      dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()