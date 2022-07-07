import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')


import pygame
import abc
import random

class Drawable(metaclass = abc.ABCMeta):
    def __init__(self, x, y, color):
        self.__x = x
        self.__y = y
        self.__color = color
        self.__visibile = True

    @abc.abstractmethod
    def draw(self, surface):
        pass

    @abc.abstractmethod
    def get_rect(self):
        pass

    def intersect(self, other):
        x11, x12, y11, y12 = self.get_rect()
        x21, x22, y21, y22 = other.get_rect()
        if (x11 < x22) and (x12 > x21) and (y11 < y22) and (y12 > y21):
            return True
        return False

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def position(self):
        return (self.__x, self.__y)

    def getColor(self):
        return self.__color

    def getVisibility(self):
        return self.__visibile

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y

    def setColor(self, color):
        self.__color = color

    def setVisibility(self, value):
        self.__visibile = value


class Ball(Drawable):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.__radius = 15
        self.__vx = 0
        self.__vy = 0

    def draw(self, surface):
        x, y = self.position()
        pygame.draw.circle(surface, self.getColor(), (int(x), int(y)), self.__radius)

    def get_rect(self):
        x, y = self.position()
        return (x - self.__radius, x + self.__radius,
                y - self.__radius, y + self.__radius)

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

class Block(Drawable):
    def __init__(self, x, y, size):
        super().__init__(x, y, (0,255,0))
        self.__size = size

    def draw(self, surface):
        x, y = self.position()
        pygame.draw.rect(surface, self.getColor(), (x, y, self.__size, -1*self.__size))
        pygame.draw.line(surface, (0,0,0), (x, y), (x + self.__size, y))
        pygame.draw.line(surface, (0,0,0), (x, y), (x, y - self.__size))
        pygame.draw.line(surface, (0,0,0), (x + self.__size, y - self.__size), (x, y - self.__size))
        pygame.draw.line(surface, (0,0,0), (x + self.__size, y - self.__size), (x + self.__size, y))

    def get_rect(self):
        x, y = self.position()
        return (x, x + self.__size, y - self.__size, y)


class Text(Drawable):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y, (0, 0, 0))
        self.__font = pygame.font.Font("freesansbold.ttf", 27)

    def get_rect(self):
        sameple = (self.__font.render('Score: ' + ' ', True, self.getColor())) #random number
        return (sample.get_width(), sample.get_height())

    def draw(self, surface, score):
        x, y = self.position()
        score_message = self.__font.render('Score: ' + str(score), True, self.getColor())
        surface.blit(score_message, self.position())

class Line():
    def __init__(self, x, y, width, height):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__sizeeight = height
        self.__color = (0,0,0)

    def draw(self, surface):
        pygame.draw.line(surface, self.__color, (int(self.__x), int(self.__y)), (int(self.__width), int(self.__sizeeight)))

    def position(self):
        return (self.__width, self.__sizeeight)

    def setX(self, x):
        self.__width = x

    def setY(self, y):
        self.__sizeeight = y
