import sys
import pygame
#import sys & pygame modules --> pygame contains functionality needed to make game
#use tools in sys module to exit game when player quits

from settings import Settings
#import settings into main program file
from ship import Ship
#import Ship

class AlienInvasion:
    #Overall class to manage game assets and behavior
    def __init__(self):
       #initialize game, and create game resources, initializes background settings
       pygame.init()
       self.settings = Settings()
       #creates instance of settings
       

       self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) 
       #creates a display window, 1200 by 800 pixels, assign to attribute self.screen
       #so available in all methods
       #object assigned to self.screen is a surface, part of screen where game element can be displayed (ex ship, alien are elements)
       #display.set_mode represents entire game window
       #when activate game animation loop, surface redraw every loop to be updated with any changes trigger by user input
       pygame.display.set_caption('Alien Invasion')

       self.ship = Ship(self) #ship class's self info
       #instance of Ship after screen has been created
       #call to ship requires one argument, an instance of AlienInvasion
       #the self argument here refers to the current instance of AlienInvasion, this is the parameter that gives Ship access to the game's resources

    def run_game(self):
        #start the main loop for the game, controls game
        while True:
            #while loop runs continually --> contains event loop and code that manages screen updates
            #watch for keyboard and mouse events
            #event is an action that user performs while playing like clicking mouse/pressing key

            self._check_events() #to call a method from within a class, use dot notation with the variable self and the name of the method
            self._update_screen()

            #while loop runs continually --> contains event loop and code that manages screen updates
            #watch for keyboard and mouse events
            #event is an action that user performs while playing like clicking mouse/pressing key
            #our event loop listen for events and perform appropriate tasks
    def _check_events(self):
        for event in pygame.event.get():
            #event loop
            #pygame.event.get() returns list of events taken place since last time function called
            #any keyboard or mouse events causes for loop to run
            #if statements to detect and repsond to specific events
            #user clicks game window's close button, call sys.exit() to exit game
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                #a keydown event is anytime a key is pressed
                if event.key == pygame.K_RIGHT:
                    #move ship to the right
                    self.ship.rect.x +=1 
    def _update_screen(self):
        #redraw the screen during each pass through the loop
        #updates images on the screen, and flip to new screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme() #draw ship on screen, bottom center
    
        #make the most recently drawn screen visible
        #continually tells pygame to make most recently drawn screen visible, illusion of smooth movement
        pygame.display.flip()

if __name__ ==  '__main__':
    #make a game instance, and run the game
    #only runs if file is called directly
    ai = AlienInvasion()
    ai.run_game()
