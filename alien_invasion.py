import sys
from time import sleep #sleep() function from time module in python so we can pause game for a moment when the ship is hit
import pygame
#import sys & pygame modules --> pygame contains functionality needed to make game
#use tools in sys module to exit game when player quits

from settings import Settings
#import settings into main program file
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
#import Ship
from bullet import Bullet
from alien import Alien

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

       #Create an instance to store game statistics
       self.stats = GameStats(self)
       self.sb = Scoreboard(self)

       self.ship = Ship(self) #ship class's self info
       #instance of Ship after screen has been created
       #call to ship requires one argument, an instance of AlienInvasion
       #the self argument here refers to the current instance of AlienInvasion, this is the parameter that gives Ship access to the game's resources

       self.bullets = pygame.sprite.Group() #an instance of the pygame.sprite.Group class, which behaves like a list with some extra functionality that is helpful
       #when writing games
       #use this group to draw bullets to the screen on each pass through the main loop and to update each bullet's position
       self.aliens = pygame.sprite.Group() #group to hold the fleet of aliens

       self._create_fleet()

       #we only need one Play button, so create button in __init__() method
       self.play_button = Button(self, "Play")
       #creates an instance of Button with the label Play, but it doesn't draw the button to the screen
       #we call button's draw_button() method to draw button to screen

    def run_game(self):
        #start the main loop for the game, controls game
        while True:
            #while loop runs continually --> contains event loop and code that manages screen updates
            #watch for keyboard and mouse events
            #event is an action that user performs while playing like clicking mouse/pressing key
            self._check_events() #to call a method from within a class, use dot notation with the variable self and the name of the method
            #need to know if user presses Q to quit or clicks buttom to close window even if game is inactive

            if self.stats.game_active:
                self.ship.update() #calls the ship's update method on each pass through the loop
                #ship's position will be updated after we've checked for keyboard events and before we update the screen
                self._update_bullets()
                #allows ship's position to be updated in response to player input and ensures the updated position will be used when drawing ship to screen
                self._update_aliens() #update position of each alien, after bullets have be updated because checking to see whether any bullets hit any aliens
                #we don't update these things because don't want game elements to update positions when game is inactive

            self._update_screen() #need to keep updating the screen even when game inactive in roder to make cahnges to screen while waiting to
            #see if player chooses to start a new game

            #print(len(self.bullets)) #shows how many bullets currently exist in the game and verify that they're being deleted when reach top of screen
            #can wathc the terminal output while firing bullets and see that the number of bullets decreases to zero after each series of bullets
            #has cleared the top of the screen
            #take out print once verify good because will slow down the game
        
            #while loop runs continually --> contains event loop and code that manages screen updates
            #watch for keyboard and mouse events
            #event is an action that user performs while playing like clicking mouse/pressing key
            #our event loop listen for events and perform appropriate tasks

    def _ship_hit(self):
        #respond to the ship being hit by an alien
        #if ships left of the three allowed are greater than 0
        if self.stats.ships_left > 0:
            #decrement ships left
            self.stats.ships_left -= 1 #each time ship hit, ship is gone so subtract one, tells us when player has run out of ships
            #get rid of any remaining aliens and bullets because alien hit ship (lost a game)
            self.aliens.empty()
            self.bullets.empty()
            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            #pause
            sleep(0.5)
            #pause after updates have been made to all game elements but before any changes have been drawn to screen
            #so player can see that the alien has hit the ship
            #sleep pauses program execution for half a second
            #when sleep() function ends, code execution moves on to the _update_screen() method, which draws the new fleet to the screen
        else:
            self.stats.game_active = False #if player has no ships left, set game_active to False
            pygame.mouse.set_visible(True) #make cursor visible again as soon as the game becomes inactive, which happens in _ship_hit()
    
    def _check_events(self):
        for event in pygame.event.get():
            #event loop
            #pygame.event.get() returns list of events taken place since last time function called
            #any keyboard or mouse events causes for loop to run
            #if statements to detect and repsond to specific events
            #user clicks game window's close button, call sys.exit() to exit game
            if event.type == pygame.QUIT:
                sys.exit()
            
            #pygame detects mouse button down event when player clicks anywhere on the screen
            #want to restrict our game to repsond to mouse click only on play button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos() #returns a tuple containing the mouse cursor's x and y coordinates when mouse button is clicked
                #we send these values to the new method _check_play_button
                self._check_play_button(mouse_pos)
            
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

        #using keyup and keydown together help make continuous motion
        #can use elif blocks here because each event is connected to only one key
        #if player presses both keys at once, two seaparate events will be detected

    def _check_play_button(self, mouse_pos):
        #start a new game when the player clicks Play
        #collidepoint checks whether point of mouse click overlaps the region defined by Play button's rect, and game is not active new game begins
        #if overlaps, set game_active to True and game begins!
        button_clicked = self.play_button.rect.collidepoint(mouse_pos) #stores a true or false value
        if button_clicked and not self.stats.game_active:
            #game only restarts if play is clicked and the game is not currently active
            #reset the game settings
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats() #restarts ship limit at 3, reset game stats
            self.stats.game_active = True #game begins as soon as the code in this function finishes running
            self.sb.prep_score() #after resetting the game stats when starting a new game, this makes scoreboard with a 0 score
            self.sb.prep_level() #make sure the new level displays correctly

            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #hide the mouse cursor when game is active
            pygame.mouse.set_visible(False) #passing False to set visible() tells pygame to hide cursor when mouse is over the game window

    def _create_fleet(self):
        #create the fleet of aliens
        #create an alien and find the number of aliens in a row
        #spacing between each alien is equal to one alien width
        #make an alien
        alien = Alien(self) #we need to know the alien's width and height to place aliens before calculations
        alien_width, alien_height = alien.rect.size #returns tuple with width and height of a rect object

        #available space is the space one alien widths off each side of the screen (margins), we have two margins (left and right side) so multiply by 2
        available_space_x = self.settings.screen_width - (2 * alien_width)
        #we just found how much space we have for ships horizontally, need to find number of ships max we can have across screen
        #its one ship plus the length of a ship for space, so its 2 x alien_width
        number_aliens_x = available_space_x // (2 * alien_width)

        #determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                                (3 * alien_height) - ship_height) #two aliens from bottom and ship from bottom, an alien from top
                                #wrapped in parenthesis so outcome can be split over two lines, which results in 79 characters or less as recommended
        number_rows = available_space_y // (2 * alien_height) #available space divided by 2 aliens height for alien and area around ship (an alien equivalent)

        #create the full fleet of aliens
        for row_number in range(number_rows):
            #create each row of aliens
            #outer loop count from 0 to the number of rows we can make (see above)
            for alien_number in range(number_aliens_x):
                #inner loop creates aliens in one row, max number aliens we can make in a row
                #create an alien and place it in the row
                #counts from 0 to the number of aliens need to make
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number): #need alien number that currently being created
        #create an alien and place in the row
        alien = Alien(self) #create new alien
        alien_width, alien_height = alien.rect.size #returns tuple with width and height of rect object
        alien.x = alien_width + 2 * alien_width * alien_number #set new alien's x coordinate value to place it in row
        #alien number is 0,1,2,3...
        #each alien is pushed to the right one alien width from the left margin
        #multiply the alien width by 2 to account for space each alien takes up, including emtpy space to the right, multiple this amount by
        #alien's position in the row
        alien.rect.x = alien.x
        #change an alien's y coordinate value when its not in the first row by starting with one alien's height to create empty space at top of screen --> if first row then its just the same
        #each row starts two alien heights below the previous row, so multiply alien height by two and then by the row number
        #first row is row number 0, so vertical placement of first row is unchanged
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien) # add each new alien to group aliens
        #creating one instance of ALien, then adding it to the group that will hold the fleet
        #the alien will be place in default upper left area of screen initially
    

    #check fleet edges loop through fleet and call check_edges in alien class on each alien
    #if check edges in alien class reutrns true, we know an alien is at an edge and the whole fleet needs to change direction, so we call change
    #fleet direction and break out of the loop
    def _check_fleet_edges(self):
        #respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    

    #in change fleet direction, we loop through all the aliens and drop each one using the setting fleet_drop_speed (drops at that speed)
    #then we change the value of fleet direction by multipling its current value by -1
    
    def _change_fleet_direction(self):
        #drop entire fleet and change the fleet's dirction
        #the line that changes the fleet's direction isn't part of the for loop
        #we want to change each alien's vertical position, but we only want to change the direction of the fleet once
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1
        #changing direction of fleet in settings

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
    
    def _update_bullets(self):
        self.bullets.update()
        #when you call automaticcaly on a group (pygame.sprite.Group), the group auto calls update() for each sprite in the group
        #the self.bullets.update() calls bullet.update() for each bullet we place in the group bullets
        #update position of bullets and get rid of old bullets
        #update bullet positions
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

        self._check_bullet_alien_collisions()

        
    def _check_bullet_alien_collisions(self):
        #respond to bullet-alien collisions
        #remove any bullets and aliens that have colided
        #check for any bullets that have hit aliens
        #if has hit alien, get rid of the bullet and the alien
        #group collide returns dictionary, each key a bullet and corresponding value is alien that was hit
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        #when bullet hits an alien, pygame returns a collisions dictionary
        #checks if collisions dictionary exists (), and if it does alien's value is added to the score
        #if collisisons dictionary exists, we loop through all values in the dictionary
        #each value is a list of aliens hit by a single bullet
        #we multiply the value of each alien by the number of aliens in each list and add this amount to the current score
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score() #create new image for the updated score
            self.sb.check_high_score() #call check high score each time an alien is hit after updating the score in check bullet collisions

        #new code compares positions of all bullets in self.bullets and all the aliens in self.aliens, and identifies any that overlap
        #whenever the rects of a bullet and alien overlap, groupcollide() adds a key value pair to dictionary it returns
        #the two arguments tell Pygame to delete the bullets and aliens that have collided
        #if you wanted a high powered bullet that can travel to the top of the screen, destroying every alien in its path, you could
        #set the fist Boolean argument to False and the second Boolean argument to True
        #the aliens hit would disappear, but all bullets would stay active until they disappeared off the top of the screen
        #whenever you run alien invasion now, aliens you hit should disappear

        #check whether the aliens group is empty
        #if returns false and alien group still has aliens, doesn't run through loop
        #if there are no aliens and returns true, runs through loop
        if not self.aliens:
            #destroy bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #increase level
            self.stats.level += 1
            self.sb.prep_level()
      
        #if alien group is empty, get rid of any existing bullets by using empty() method which removes all the remaining sprites of the group of bullets
        #also make create_fleet() which fills the screen with aliens again

    def _check_aliens_bottom(self):
        #check if any aliens ahve reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat this the same as if the ship got hit
                self._ship_hit()
                break

        #check whether any aliens have reached the bottom of the screen
        #an alien reaches the bottom whit its rect.bottom value is greater than or equal to the screen's rect.bottom attribute
        #if an alien touches the bottom, we call _ship_hit()
        #if one alien touches the bottom theres no need to check the rest so break out of loop and call ship hit()

    def _update_aliens(self):
        #check if fleet is at an edge, then update the position of all aliens in the fleet
        #update the positions of all aliens in the fleet
        self._check_fleet_edges() #check edges before updating alien's position
        self.aliens.update() #use the update method on the aliens group, which calls each alien's update() method, making fleet move right

        #the spritecollideny() function takes two arguments - a sprite and a group
        #looks for any member of the group that has collided with the sprite and stops looking through the group as soon as it finds one memeber
        #that has collided with the sprite
        #loops through group aliens and returns the first alien it finds that has collided with the ship
        #if no collisions occur, spritecollidenay() returns None and the if block won't exeute
        #if  spritecollideany() finds an alien that has collided with the ship, it returns that alien and the if block executes
        #goes to _ship_hit() method
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
        #call check aliens bottom after updating the positions of all the aliens and after looking for alien and ship collisions
        #now a new fleet will appear every time the ship is hit by an alien or an alien reaches the bottom of the screen
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
        
        #to make alien appear, need to call the group's draw() method
        self.aliens.draw(self.screen)
        #when call draw() on a group, pygame draws each element in the group at the position defined by its rect attribute
        #draw method requires one argument - surface on which to draw the elements from the group

        #draw the score information
        self.sb.show_score()

        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        #to make the Play button visible above all other elements on screen, we draw it after all the other elements have been drawn
        #but before flipping to a new screen
        #we include an if block so button only appears when the game is inactive

        pygame.display.flip()

if __name__ ==  '__main__':
    #make a game instance, and run the game
    #only runs if file is called directly
    ai = AlienInvasion()
    ai.run_game()
