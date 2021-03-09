#to use our ship, have ship module that will contain the class Ship
#Ship class will manage most of the behavior of player's ship
import pygame

class Ship:
    #a class to manage the ship

    def __init__(self, ai_game):
        #self reference and reference to current instance of AlienInvasion class
        #gives Ship access to all game resources defined in AlienInvasion
        #intialize the ship and set its starting position
        self.screen = ai_game.screen #assign screen to attribute of ship to access easily in all methods of Ship class
        self.screen_rect = ai_game.screen.get_rect() #access the screen's rect attribute, allows us to place ship in correct location on screen

        #load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp') #returns surfae representing the ship, which we assign to self.image
        self.rect = self.image.get_rect() #access the ship's surface rect attribute so we can later use it to place ship

        #start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        #position ship at bottom center of screen
        #make value of self.rect.midbottom match the midbottom attribute of screen's rect

        self.moving_right = False #when false ship is motionless
        self.moving_left = False

    def update(self):
        #update the ship's position based on the movement flag
        #called through an instance of Ship, so not considered a helper method
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1
    #use two separate blocks rather than an elif to allow ship's rect.x value to be increased and then decreased when both arrow keys held down -->result is stand still
    #if had used elif for motion to the left, the right arrow key would always have priority


    def blitme(self):
        #draw the ship at its curent loaction specified by self.rect
        self.screen.blit(self.image, self.rect)


#pygame is efficient because lets treat all game elements like rectangles (rects)
#shdn pygame needs to figure out whether two game elements have collided, it can do this more quickly by treating each object as rectangle
#treat ship and screen as rectangles in this class

#when working with rect object - use x and y coordinates of top,bottom, left, and right edges of rectangle as well as center
#can set any of these values of rect to establish current position of rect
#when centering game element, work with teh center, centerx, or centery attributes of rect
#when working with edge of screen, work with top, bottom, left, or right attributes
#also attributes that combine properties, such as midbottom, midtop, midleft, and midright
#when adjusting horizontal or vertal placement of rect, use x and y attributes, which are the x and y coordinates of its to left corner
#attributes spare you from having to do calculations that gmae developers formerly had to do manually
#on 1200 by 800 screen, origin at top left corner (0,0) and bottom right corner is (1200,800) --> refer to game window, not physical screen
