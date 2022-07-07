import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')
# My path variable with python is messed up, this is included so I can access pygames, but is edited out so it doesn't influence your python


'''
Name: Christopher Morris
Id: 14289223
'''

import pygame
from text import Text
from ball import Ball
from block import Block

#Class made to handle all of the objects that are called
class UserObjects():
    def __init__(self, height, width, radius, block_size, num_block):
        self.__screen_height = height
        self.__screen_width  = width
        self.__ball_radius = radius
        self.__block_size = block_size
        self.__num_boxes = num_block
        self.__score = 0
        self.__display = [Text(self)] #score
        self.__background = [BackgroundLine(int(height * 3/4), width)] #horizontal line
        self.__blocks = []
        self.__balls = []
        self.makeBlocks()

    def makeBlocks(self): #Funciton that makes blocks based on given number of blocks and returns that number squared
        for i in range(self.__num_boxes):
            for j in range(self.__num_boxes):
                self.__blocks.append(Block(self.__screen_width * (2/3) + self.__block_size*i,
                                     self.__background[0].getY() - self.__block_size*j, self.__block_size))

    def setBalls(self, Ball): #add balls
        self.__balls.append(Ball)

    def getBalls(self):
        return self.__balls

    def getLine(self):
        return self.__background[0]

    def getBlocks(self):
        return self.__blocks

    def getObjects(self): #Returns all objects in the user class
        return self.__background + self.__blocks + self.__balls + self.__display

    def getScore(self):
        return self.__score

    def getScreenWidth(self):
        return self.__screen_width

    def incrementScore(self): #everytime a block is hit the score is increased
        self.__score += 1

class BackgroundLine(): #simple line for the background.
    def __init__(self, y, width):
        self.__x = 0
        self.__y = y
        self.__width = width

    def draw(self, surface):
        pygame.draw.line(surface, (0,0,0), (int(self.__x), int(self.__y)), (int(self.__x + self.__width), int(self.__y )))

    def getY(self):
        return self.__y
