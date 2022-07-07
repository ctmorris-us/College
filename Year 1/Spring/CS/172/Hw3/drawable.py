import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')
# My path variable with python is messed up, this is included so I can access pygames, but is edited out so it doesn't influence your python


'''
Name: Christopher Morris
Id: 14289223
'''

import pygame
import abc

# Main drawable class
class Drawable(metaclass = abc.ABCMeta):
    def __init__(self, x, y, color):
        self.__x = x
        self.__y = y
        self.__color = color
        self.__visibile = True #Not used

    @abc.abstractmethod
    def draw(self, surface):
        pass

    @abc.abstractmethod
    def get_rect(self):
        pass

    def get_intersection(self, other): #Gets two rectangles and goes from left, bottom to right, upper points.
        x1lower, x1upper, y1lower, y1upper = self.get_rect()
        x2lower, x2upper, y2lower, y2upper = other.get_rect()

        if (x2lower <= x1upper <= x2upper) or (x1lower <= x2upper <= x1upper):
            if (y2upper <= y1lower <= y2lower) or (y1upper <= y2lower <= y1lower):
                return True
        else:
            return False

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getColor(self):
        return self.__color

    def getVisibility(self): #Not used but needed to include
        return self.__visibile

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y

    def setColor(self, color):
        self.__color = color

    def setVisibility(self, value): #Not used but needed to include
        self.__visibile = value
