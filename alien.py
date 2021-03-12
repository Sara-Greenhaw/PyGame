import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    #a class to represent a single alien in the fleet

    def __init__(self, ai_game):
        #initialize the alien and set its starting position

        super().__init__() #not sure what this does 
        self.screen = ai_game.screen

        #load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #start each new alien near the top left of the screen
        #default top left is (0, 0) on screen, so don't need to specify it starting a certain place because default is where we want it!
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #store the alien's exact horizontal position
        self.x = float(self.rect.x)


    #the alien class doesn't need a method for drawing it to the screen - instead we will use a pygame method that automatically draws all
    #all the elemnts of a group to the screen