import sys
import pygame

class AlienInvasion:
    #Overall class to manage game assets and behavior
    def __init__(self):
       #initialize game, and create game resourcres
       pygame.int()

       self.screen = pygame.display.set_mode((1200,800))
       pygame.display.set_caption('alien invasion')

    def run_game(self):
        #start the main loop for the game
        while True:
            #watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #make the most recently drawn screen visible 
            pygame.display.flip()

if __name__ ==  '__main__':
    #make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
