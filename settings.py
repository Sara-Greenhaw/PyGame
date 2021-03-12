#instead of adding settings throughout code, store all settings values in one place
#work with one setting object any time need to access individ setting
#easier to modify game appearance as project grows
class Settings:
    #a class to store all settings for alien invasion

    def __init__(self):
        #initialize game's settings
        #screen settings
        self.screen_width = 1200
        self.screen_height = 625
        #800 to tall for my screen so made 625
        self.bg_color = (230, 230, 230)

        #ship setings --> making faster. Originally moving 1 pixel per cycle, now 1.5 pixels per cycle
        self.ship_speed = 1.5

        #bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        #these setting create dark gray bullets with a width of 3 pixels and a height of 15 pixels, bullets will travel slightly slower than ship
        #limit the number of bullets a player can have on the screen at a time
        #this limits the player to three bullets at a time
        self.bullets_allowed = 3
        #alien settings
        self.alien_speed = 1.0
