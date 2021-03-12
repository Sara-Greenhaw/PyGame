class GameStats:
    #track statistics for Alien Invasion

    def __init__(self, ai_game):
        #initialize statistics
        #make one Gamestats instance for the entire time Alien Invasion is running
        self.settings = ai_game.settings
        self.reset_stats()

    #we need to reset statistcs each time the player starts a new game
    #call reset_stats called anytime the player starts a new game
    def reset_stats(self):
        #intialize statistics that can change during the game
        self.ships_left = self.settings.ship_limit