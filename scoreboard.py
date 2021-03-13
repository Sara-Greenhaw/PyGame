import pygame.font
from pygame.sprite import Group

from ship import Ship #making group of ships so import Group and Ship classes
#because scoreboard writes text to the screen, we begin by importing the pygame.font module

class Scoreboard:
    #a class to report scoring ifnormation

    def __init__(self, ai_game):
        #give __init__() the ai_game parameter so it can access the settings, screen, and stats object which it will need to 
        #report the value we're tracking
        #initalize scorekeeping attributes
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #font settings for scoring information
        self.text_color = (30, 30, 30) #set text color
        self.font = pygame.font.SysFont(None, 48) #instantiate a font object, none argument tells pygame to use the default font, and 48 specifies the size of text

        #prepare the intitial score images
        #turn text into an image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        #turn the score into a rendered image
        #the round() function normally rounds a decimal number to a set number of decimal places given as second argument
        #when you pass a negative number as the second argument, round() will round the value ot the nearest 10,100,1000, and so on
        rounded_score = round(self.stats.score, -1) #tells python to round the value of stats.score ot the nearest 10 and store it in rounded_score
        score_str = "{:,}".format(rounded_score) #tells python to insert commas into numbers when converting a numerical value into string (1,000,000 instead of 1000000)
        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)
                #render creates an image
                #the font.render() method also takes  a boolean value to turn antialiasing on or off (make edges of text smoother), then font color and background color
                
        #display the score at the top right of screen
        #we position the score in the upper-right corner of the screen and have it expand to the left as the score increases and width of number grows
        self.score_rect = self.score_image.get_rect() 
        self.score_rect.right = self.screen_rect.right - 20 #set right edge rect of score image 20 pixels down from the right edge of the screen
        self.score_rect.top = 20 #set top edge of rect of score image 20 pixels from the top of the screen

    def show_score(self):
        #draw score, high score, and level to the screen 
        self.screen.blit(self.score_image, self.score_rect) #draws the score image onscreen at the location score_rect specifies --> top right
        self.screen.blit(self.high_score_image, self.high_score_rect) #draws high score top center of screen
        self.screen.blit(self.level_image, self.level_rect) #draws level image to screen
        self.ships.draw(self.screen) #display the ships on screen, and pygame draws each ship


    def prep_high_score(self):
        #turn high score into a rendered image
        high_score = round(self.stats.high_score, -1) #rounds high score to nearest 10 and formats with commas
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color) #generate image from the high score

        #center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx #center the high score horizontally
        self.high_score_rect.top = self.score_rect.top #set top attribute of high score image to top of score image (20 pixels from top of screen)

    def check_high_score(self):
        #check to see if there's a new high score
        #if current score is greater, update the value of high_score and call prep_high_score() to update the high score's image
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        #turn the level into a rendered image
        level_str = str(self.stats.level)
        #create an image from the value stored in stats.level
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        #position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right #set image of level's right attribute to match the score's right attribute
        self.level_rect.top = self.score_rect.bottom + 10 #sets the top attribute of image level 10 pixels beneath the bottom of the score image
        #to leave space between the score and the level

    def prep_ships(self):
        #show how many ships are left
        self.ships = Group() #creates an empty group, self.ships, to hold the ship instances
        #to fill the self.ships group, a loop runs once for every ship the player has left
        for ship_number in range(self.stats.ships_left):
            #inside loop, we create a new ship and set each ship's x coord value so the ships appear next to each other w a 10 pixel margin
            #on left side of the group of ships
            #we set y coord value 10 pixels down from the top of the screen so the ships appear in the upper-left corner of the screen
            #then we add each new ship to the group of ships
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
    
