import pygame.font #lets pygame render text to the screen
class Button:
    def __init__(self, ai_game, msg):
        #initialize button attributes
        #msg contains button's text
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #set the dimensions and properties of the button
        #order of colors (red, green, blue)
        self.width, self.height = 200, 50 #dimensions of box
        self.button_color = (0, 255, 0) #bright green
        self.text_color = (255, 255, 255) #white text
        self.font = pygame.font.SysFont(None, 48) #none argument tells pygame to use the default font, and 48 specifies the size of textt

        #build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height) #initialize rect at (0,0) with the widht and height
        self.rect.center = self.screen_rect.center #assign button's rect to the center of the screen

        #pygame works with text by rendering the string you want to display as an image
        #the button message needs to be prepped only once
        self._prep_msg(msg) #handles rendering

        def _prep_msg(self, msg):
            #turn msg into a rendered image and center text on the buttom
            #msg is the text that needs to be rendered as an image
            #self.font.render() turns text stored in msg into an image, which we then store in the self.msg_image
            #the font.render() method also takes  aboolean value to turn antialiasing on or off (make edges of text smoother), then font color and background color
            #we set antialiasing to True and set the text background to same color as the button
            self.msg_image = self.font.render(msg, True, self.text_color,
                    self.button_color)
            self.msg_image_rect = self.msg_image.get_rect()
            self.msg_image_rect.center = self.rect.center #center text image on the button by creating a rect from the image and settings its center attribute to
            #match that of the button

            def draw_button(self):
                #draw blank buttona dn then draw message
                self.screen.fill(self.button_color, self.rect) #draw the rectangular portion of the button
                self.screen.blit(self.msg_image, self.msg_image_rect) #draw the text image to the screen, passing it an image and the rect object associated with the image


