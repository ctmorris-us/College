import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')


import pygame
import abc
import random

class Drawable(metaclass = abc.ABCMeta):
	def __init__(self,x=0,y=0):
		self.__x=x
		self.__y=y

	def getLocx(self):
		return self.__x

	def getLocy(self):
		return self.__y

	def setLoc(self,p):
		self.__x = p[0]
		self.__y = p[1]

	@abc.abstractmethod
	def draw(self,surface):
		pass

class Rectangle(Drawable):
	def __init__(self, x, y, width, height, color):
		super().__init__(x, y)
		self.__width = width
		self.__height = height
		self.__color = color

	def draw(self, surface):
		pygame.draw.rect(surface, self.__color, (self.getLocx(), self.getLocy(), self.__width, self.__height))


class Snowflake(Drawable):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.setMax()

	def draw(self, surface):
		pygame.draw.line(surface, (255,255,255), (self.getLocx() - 5, self.getLocy()), (self.getLocx() + 5, self.getLocy()))
		pygame.draw.line(surface, (255,255,255), (self.getLocx() - 5, self.getLocy() - 5), (self.getLocx() + 5, self.getLocy() + 5))
		pygame.draw.line(surface, (255,255,255), (self.getLocx() - 5, self.getLocy() + 5), (self.getLocx() + 5, self.getLocy() - 5))
		pygame.draw.line(surface, (255,255,255), (self.getLocx(), self.getLocy() - 5), (self.getLocx(), self.getLocy() + 5))

	def setMax(self):
		self.__max = random.randint(275, 375)

	def getMax(self):
		return self.__max

random.seed(100)

pygame.init()
surface = pygame.display.set_mode((400, 400))

objects = []
objects.append(Rectangle(0, 250, 400, 150, (0, 255, 0)))
objects.append(Rectangle(0, 0, 400, 250, (0,150,255)))
for i in range(5):
	objects.append(Snowflake(random.randint(0,400), 0))

clock = pygame.time.Clock()
while True:
	surface.fill((0,0,0))

	for event in pygame.event.get():
		if (event.type == pygame.KEYDOWN and event.__dict__['key'] == pygame.K_SPACE):
			flag = True
			while flag:
				events = pygame.event.get()
				if len(events) != 0:
					for event in events:
						if (event.type == pygame.KEYDOWN and event.__dict__['key'] == pygame.K_SPACE):
							flag = False

	for o in objects:
		if isinstance(o, Snowflake):
			if o.getLocy() < o.getMax():
				o.setLoc([o.getLocx(), o.getLocy() + 5])

	for i in range(random.randint(0,4)):
		objects.append(Snowflake(random.randint(0,400), 0))

	for o in objects:
		o.draw(surface)

	pygame.display.update()
	clock.tick(30)
