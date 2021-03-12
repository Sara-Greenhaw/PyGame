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