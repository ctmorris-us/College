import math

class Shape():

    bad_list = []
    good_list = []
    unavaiable = []

    def __init__(self, name, type):
        self.a = setSide('a', name, type, 1)
        self.b = setSide('b', name, type, 1)
        self.c = setSide('c', name, type, 1)
        self.d = setSide('d', name, type, 1)
        self.e = setSide('e', name, type, math.sqrt(2))

    def setSide(self, name_side, name_shape, type, length_side):
        self.name_side = (name_side, name_shape, type, length_side)

    def getNext(self, value): #counter clockwise
        pass

    @staticmethod
    def addBad(self, value):
        pass

    @staticmethod
    def addGood(self, value):
        pass

    @staticmethod
    def addUnavailable(self, value): #append new list with ID of both intersections new list per new shape
        pass

    @staticmethod
    def delUnavaiable(self, value):
        pass

    def checkIntersection(self, other): #Go around shape
        pass


class shape1():
    def __init__(self, name):
        self.name = name
        self.type = 1
        super().__init__(self.name, self.type )
        self.straight = [(self.c, self.d)]

    def order(self):
        return ('a', 'b', 'c', 'd', 'e')

    def setName(self):
        self.name = ''
