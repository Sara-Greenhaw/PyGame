import pygame.font
#because scoreboard writes text to the screen, we begin by importing the pygame.font module

class Scoreboard:
    #a class to report scoring ifnormation

    def __init__(self, ai_game):
        #give __init__() the ai_game parameter so it can access the settings, screen, and stats object which it will need to 
        #report the value we're tracking
        #initalize scorekeeping attributes
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #font settings for scoring information
        self.text_color = (30, 30, 30) #set text color
        self.font = pygame.font.SysFont(None, 48) #instantiate a font object, none argument tells pygame to use the default font, and 48 specifies the size of text

        #prepare the intitial score image
        #turn text into an image
        self.prep_score()

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
        #draw score to the screen
        self.screen.blit(self.score_image, self.score_rect) #draws the score image onscreen at the location score_rect specifies