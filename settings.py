#instead of adding settings throughout code, store all settings values in one place
#work with one setting object any time need to access individ setting
#easier to modify game appearance as project grows
class Settings:
    #a class to store all settings for alien invasion

    def __init__(self):
        #initialize game's static settings
        #screen settings
        self.screen_width = 1200
        self.screen_height = 625
        #800 to tall for my screen so made 625
        self.bg_color = (230, 230, 230)

        #ship setings 
        self.ship_limit  = 2 #the number of ships the player starts out with
        #assigning 3 made 4 ships

        #bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        #these setting create dark gray bullets with a width of 3 pixels and a height of 15 pixels, bullets will travel slightly slower than ship
        #limit the number of bullets a player can have on the screen at a time
        #this limits the player to three bullets at a time
        self.bullets_allowed = 3

        #alien settings
        self.fleet_drop_speed = 10 #controls how quickly the fleet drops down the screen each time an alien reaches either edge
        #helpful to separate drop speed from horizontal speed so you can adjust the two speed independently
        #dont need to increase the speed of fleet drop spee dbecause when aliens move faster across screen they'll also come down screen faster

        #how quickly the game speeds up
        self.speedup_scale = 1.1 #speeds up game speed every time the player reaches a new level, value of 1 would keep speed constant

        #how quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings() #method to initialize the values for attributes that need to change throughout the game


    def initialize_dynamic_settings(self):
        #intialize settings that change throughout the game
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        #fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        #scoring
        self.alien_points = 50

    def increase_speed(self):
        #increase speed settings and alien point values
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        #to increase the speed of these elemens, we multiply each speed setting byt he value of speedup_scale in _init__()

        self.alien_points = int(self.alien_points * self.score_scale)
        #verify seeing point of alien value each new level
        #print(self.alien_points) --> removed after checking


