import sys
import pygame
#import sys & pygame modules --> pygame contains functionality needed to make game
#use tools in sys module to exit game when player quits

from settings import Settings
#import settings into main program file
from ship import Ship
#import Ship
from bullet import Bullet

class AlienInvasion:
    #Overall class to manage game assets and behavior
    def __init__(self):
       #initialize game, and create game resources, initializes background settings
       pygame.init()
       self.settings = Settings()
       #creates instance of settings

       self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #tells pygame to figure out a window size that will fill the screen
       self.settings.screen_width = self.screen.get_rect().width
       self.settings.screen_height = self. screen. get_rect().height 

       #self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) 
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

       self.bullets = pygame.sprite.Group() #an instance of the pygame.sprite.Group class, which behaves like a list with some extra functionality that is helpful
       #when writing games
       #use this group to draw bullets to the screen on each pass through the main loop and to update each bullet's position

    def run_game(self):
        #start the main loop for the game, controls game
        while True:
            #while loop runs continually --> contains event loop and code that manages screen updates
            #watch for keyboard and mouse events
            #event is an action that user performs while playing like clicking mouse/pressing key

            self._check_events() #to call a method from within a class, use dot notation with the variable self and the name of the method
            self.ship.update() #calls the ship's update method on each pass through the loop
            #ship's position will be updated after we've checked for keyboard events and before we update the screen
            #allows ship's position to be updated in response to player input and ensures the updated position will be used when drawing ship to screen
            self._update_screen()
            self.bullets.update() #when you call automaticcaly on a group (pygame.sprite.Group), the group auto calls update() for each sprite in the group
            #the self.bullets.update() calls bullet.update() for each bullet we place in the group bullets

            #want to get rid of old bullets because contiue to exist and consume memory and processing power, remove bullet to prevent game from slowing down
            #need to detect when the bottom value of a bullet's rect hasa  value of 0, which indicates the bullet has passed off the top of the screen
            #because you use a for loop with a list (sprite group in pygame), python expects that the list will stay the saem length as long
            #as the loop is running 
            #we can't remove items from a list or group within a for loop, we have to loop over a copy of the group
            #copy in for loop enables us to modify bullets inside the loop --> can't modify group or list in for loop, but can modify copy
            #we check each bullet to see whether it has disappeared off the top of the screen in the if statement, if it has we remove bullet
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            #print(len(self.bullets)) #shows how many bullets currently exist in the game and verify that they're being deleted when reach top of screen
            #can wathc the terminal output while firing bullets and see that the number of bullets decreases to zero after each series of bullets
            #has cleared the top of the screen
            #take out print once verify good because will slow down the game
        
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
            
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            
            
        #using keyup and keydown together help make continuous motion
        #can use elif blocks here because each event is connected to only one key
        #if player presses both keys at once, two seaparate events will be detected

    def _check_keydown_events(self, event):
        #a keydown event is anytime a key is pressed
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
            #doesn't move ship directly yet, just makes true
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        #respond to key release
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False 

        #nothing happens when spacebar is released with firing bullets

    def _fire_bullet(self):
        #create a new bullet adn add it to the bullets group
        if len (self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self) #instance of bullet and call it new_bullet --> just like we did at top with settings!
            self.bullets.add(new_bullet) #we add it to the new group bullets using the add() method
        #the add method is similar to append(), but its a method that's written just for pygame groups
    
        

    def _update_screen(self):
        #redraw the screen during each pass through the loop
        #updates images on the screen, and flip to new screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme() #draw ship on screen, bottom center

        #make sure each bullet drawn to screen before flip
        #bullets.sprites() method returns a list of all sprite in the group bullets
        #to draw all fired bullets to the screen, we loop through the sprites in bullets and call draw_bullet on each one
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #make the most recently drawn screen visible
        #continually tells pygame to make most recently drawn screen visible, illusion of smooth movement
        pygame.display.flip()

if __name__ ==  '__main__':
    #make a game instance, and run the game
    #only runs if file is called directly
    ai = AlienInvasion()
    ai.run_game()
