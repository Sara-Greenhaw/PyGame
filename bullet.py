import pygame
from pygame.sprite import Sprite
#bullet class iherits from sprite, which we import from pygame.sprite module
#when use sprite, can group related elements in your game and act on all the grouped elements at once


class Bullet(Sprite):
    #a class to manage bullets fired from ship

    def __init__(self, ai_game):
        #create a bullet object at the ship's current position
        #current instance of AlienInvasion, and we call super to inherit properly from Sprite
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #create a bullet rect at (0,0) and then set correct position
        #create bulet's rect attribute, isn't based on image so have to build rect from scratch using pygame.Rect() class
        #pygame.Rect() calss requires the x and y coordinates of the top-left corner of the rect, and the width and height of the rect
        #initialize rect at (0,0) but we'll move it to the correct location next line
        #we get width and height of the bullet form the values stored in self.settings
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.setting.bullet_height)

        self.rect.midtop = ai_game.ship.rect.midtop #bullet's midtop attribute to match the ship's midtop attribute
        #makes bullet emerge from the top of the ship, making it look like the bullet is fired from the ship

        #we store a decimal value for the bullet's y coordinate so we can make fine adjustments to the bullet's speed
        self.y = float(self.rect.y)
    
    def update(self):
        #changes the bulet's position
        #when bullet is fired, moves up the screen, which corresponds to a decreasing y-coordinate value
        #to update the position, we subtract the amount stored in settings.bullet_speed for self.y
        #bullet_speed settings allows us to increase the speed of the bullets as the game progresses or as needed to refine the game's behavior
        #once a bullet is fired, we neer change the value of its x coordinate, so it will travel vertically in a straight line even if ship moves
        #move the bullet up the screen
        #update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        #update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        #draw the bullet ot the screen
        pygame.draw.rect(self.screen, self.color, self.rect)


        