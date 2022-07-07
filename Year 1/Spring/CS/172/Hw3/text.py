import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')
# My path variable with python is messed up, this is included so I can access pygames, but is edited out so it doesn't influence your python


'''
Name: Christopher Morris
Id: 14289223
'''

import pygame
from drawable import Drawable

class Text(Drawable):
    def __init__(self, User, x = 0, y = 0):
        super().__init__(x, y, (0, 0, 0))
        self.__font = pygame.font.Font("freesansbold.ttf", 32)
        self.__user = User

    def get_rect(self): #Finds width and height of text based on what is printed, but it is not used
        text = (self.__font.render("Score: {}".format(self.__user.getScore()), True, self.getColor()))
        return (text.get_width(), text.get_height())

    def draw(self, surface): #Prints out text on top left corner of screen.
        score_message = self.__font.render("Score: {}".format(self.__user.getScore()), True, self.getColor())
        surface.blit(score_message, (self.getX(), self.getY()))
