import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')
# My path variable with python is messed up, this is included so I can access pygames, but is edited out so it doesn't influence your python


'''
Name: Christopher Morris
Id: 14289223
'''

import pygame
from drawable import Drawable

class Block(Drawable):
    def __init__(self, x, y, h):
        super().__init__(x, y, (0,255,0))
        self.__h = h #height/lenght of one side (same because it's a square)

    def draw(self, surface): #Draws rectangle and surrounding lines
        pygame.draw.rect(surface, self.getColor(), (self.getX(), self.getY(), self.getH(), -1*self.getH()))
        pygame.draw.line(surface, (0,0,0), (self.getX(), self.getY()), (self.getX() + self.getH(), self.getY()))
        pygame.draw.line(surface, (0,0,0), (self.getX(), self.getY()), (self.getX(), self.getY() - self.getH()))
        pygame.draw.line(surface, (0,0,0), (self.getX() + self.getH(), self.getY() - self.getH()), (self.getX(), self.getY() - self.getH()))
        pygame.draw.line(surface, (0,0,0), (self.getX() + self.getH(), self.getY() - self.getH()), (self.getX() + self.getH(), self.getY()))


    def get_rect(self):
        return (self.getX(), self.getX() + self.getH(),
                self.getY(), self.getY() - self.getH())

    def getH(self):
        return self.__h
