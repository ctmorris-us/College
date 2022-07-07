import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')
# My path variable with python is messed up, this is included so I can access pygames, but is edited out so it doesn't influence your python


'''
Name: Christopher Morris
Id: 14289223
'''

import pygame
from drawable import Drawable

class Ball(Drawable):
    def __init__(self, x, y, radius):
        super().__init__(x, y, (0,0, 255))
        self.__radius = radius
        self.__vx = 0
        self.__vy = 0

    def draw(self, surface): #From abstract base class
        pygame.draw.circle(surface, self.getColor(), (int(self.getX()), int(self.getY())), self.getRadius())

    def get_rect(self): #rectangle from left to right and bottom to top.
        return (self.getX() - self.getRadius(), self.getX ()+ self.getRadius(),
                self.getY() + self.getRadius(), self.getY() - self.getRadius())

    def getRadius(self):
        return self.__radius

    def getVX(self):
        return self.__vx

    def getVY(self):
        return self.__vy

    def setVX(self, vx):
        self.__vx = vx

    def setVY(self, vy):
        self.__vy = vy
