#Mark Boady and Matthew Burlick
#Drexel University 2018
#CS 172


#This class defines a generic monster
#It doesn't actually DO anything.
#It just gives you a template for how a monster works.

#We can make any number of monsters and have them fight
#they just all need to INHERIT from this one so that work the same way

#Since this class is not intended to be used
#none of the methods do anything
#This class is cannot be used by itself.
import abc

class monster(metaclass=abc.ABCMeta):
	def __init__(self):
		return
	def __str__(self):
		return "Generic Monster Class"
	#Methods that need to be implemented
	#The description is printed at the start to give
	#additional details

	#Name the monster we are fighting
	#The description is printed at the start to give
	#additional details
	@abc.abstractmethod
	def getName(self):
		pass

	@abc.abstractmethod
	def getDescription(self):
		pass

	#Basic Attack Move
	#This will be the most common attack the monster makes
	#You are passed the monster you are fighting
	@abc.abstractmethod
	def basicAttack(self,enemy):
		pass

	#Print the name of the attack used
	@abc.abstractmethod
	def basicName(self):
		pass

	#Defense Move
	#This move is used less frequently to
	#let the monster defend itself
	@abc.abstractmethod
	def defenseAttack(self,enemy):
		pass

	#Print out the name of the attack used
	@abc.abstractmethod
	def defenseName(self):
		pass

	#Special Attack
	#This move is used less frequently
	#but is the most powerful move the monster has
	@abc.abstractmethod
	def specialAttack(self,enemy):
		pass

	@abc.abstractmethod
	def specialName(self):
		pass

	#Health Management
	#A monster at health <= 0 is unconscious
	#This returns the current health level
	@abc.abstractmethod
	def getHealth(self):
		pass

	#This function is used by the other monster to
	#either do damage (positive int) or heal (negative int)
	@abc.abstractmethod
	def doDamage(self,damage):
		pass

	#Reset Health for next match
	@abc.abstractmethod
	def resetHealth(self):
		pass

class Dragon(monster):
	def __init__(self, name):
		self.__name = name
		self.__health = 20
		self.__defense = 0

	def __str__(self):
		return '{}: {}'.format(self.getName(), self.getDescription())
	#Name the monster we are fighting
	#The description is printed at the start to give
	#additional details
	def getName(self):
		return self.__name

	def getDescription(self):
		return 'A large, firebreathing, beast that soars through the sky and terrorizes everyone around it.'
	#Basic Attack Move
	#This will be the most common attack the monster makes
	#You are passed the monster you are fighting
	def basicAttack(self,enemy):
		print('{} used {} on {}'.format(self.getName(), self.basicName(), enemy.getName()))
		enemy.doDamage(2)

	#Print the name of the attack used
	def basicName(self):
		return 'Slash'
	#Defense Move
	#This move is used less frequently to
	#let the monster defend itself
	def defenseAttack(self,enemy):
		print('{} used {} on {}'.format(self.getName(), self.defenseName(), enemy.getName()))
		self.__defense -= 1

	#Print out the name of the attack used
	def defenseName(self):
		return 'Wing Shield'
	#Special Attack
	#This move is used less frequently
	#but is the most powerful move the monster has
	def specialAttack(self,enemy):
		print('{} used {} on {}'.format(self.getName(), self.specialName(), enemy.getName()))
		enemy.doDamage(3)

	def specialName(self):
		return 'Blazing Fire'

	#Health Management
	#A monster at health <= 0 is unconscious
	#This returns the current health level
	def getHealth(self):
		return self.__health

	#This function is used by the other monster to
	#either do damage (positive int) or heal (negative int)
	def doDamage(self,damage):
		self.__health -= damage + self.__defense
		self.__defense = 0

	#Reset Health for next match
	def resetHealth(self):
		self.__health = 20


class Serpent(monster):
	def __init__(self, name):
		self.__name = name
		self.__health = 20
		self.__defense = 0
	def __str__(self):
		return '{}: {}'.format(self.getName(), self.getDescription())

	#Name the monster we are fighting
	#The description is printed at the start to give
	#additional details
	def getName(self):
		return self.__name

	def getDescription(self):
		return 'An underwater, massive creature that rules the seas.'
	#Basic Attack Move
	#This will be the most common attack the monster makes
	#You are passed the monster you are fighting
	def basicAttack(self,enemy):
		print('{} used {} on {}'.format(self.getName(), self.basicName(), enemy.getName()))
		enemy.doDamage(2)
	#Print the name of the attack used
	def basicName(self):
		return 'Whip'

	#Defense Move
	#This move is used less frequently to
	#let the monster defend itself
	def defenseAttack(self,enemy):
		print('{} used {} on {}'.format(self.getName(), self.defenseName(), enemy.getName()))
		self.__defense -= 1

	#Print out the name of the attack used
	def defenseName(self):
		return 'Dive'

	#Special Attack
	#This move is used less frequently
	#but is the most powerful move the monster has
	def specialAttack(self,enemy):
		print('{} used {} on {}'.format(self.getName(), self.specialName(), enemy.getName()))
		enemy.doDamage(3)

	def specialName(self):
		return 'Water Gun'

	#Health Management
	#A monster at health <= 0 is unconscious
	#This returns the current health level
	def getHealth(self):
		return self.__health

	#This function is used by the other monster to
	#either do damage (positive int) or heal (negative int)
	def doDamage(self,damage):
		self.__health -= damage + self.__defense
		self.__defense = 0

	#Reset Health for next match
	def resetHealth(self):
		self.__health = 20

class Charzard(monster):
	def __init__(self, name):
		self.__name = name
		self.__health = 20
		self.__defense = 0
	def __str__(self):
		return '{}: {}'.format(self.getName(), self.getDescription())

	#Name the monster we are fighting
	#The description is printed at the start to give
	#additional details
	def getName(self):
		return self.__name

	def getDescription(self):
		return 'The Fire Starter Pokemon'
	#Basic Attack Move
	#This will be the most common attack the monster makes
	#You are passed the monster you are fighting
	def basicAttack(self,enemy):
		print('{} used {} on {}'.format(self.getName(), self.basicName(), enemy.getName()))
		enemy.doDamage(2)
	#Print the name of the attack used
	def basicName(self):
		return 'Flamethrower'

	#Defense Move
	#This move is used less frequently to
	#let the monster defend itself
	def defenseAttack(self,enemy):
		print('{} used {} on {}'.format(self.getName(), self.defenseName(), enemy.getName()))
		self.__defense -= 1

	#Print out the name of the attack used
	def defenseName(self):
		return 'Protect'

	#Special Attack
	#This move is used less frequently
	#but is the most powerful move the monster has
	def specialAttack(self,enemy):
		print('{} used {} on {}'.format(self.getName(), self.specialName(), enemy.getName()))
		enemy.doDamage(3)

	def specialName(self):
		return 'Fire Blast'

	#Health Management
	#A monster at health <= 0 is unconscious
	#This returns the current health level
	def getHealth(self):
		return self.__health

	#This function is used by the other monster to
	#either do damage (positive int) or heal (negative int)
	def doDamage(self,damage):
		self.__health -= damage + self.__defense
		self.__defense = 0

	#Reset Health for next match
	def resetHealth(self):
		self.__health = 20

class Blastoise(monster):
	def __init__(self, name):
		self.__name = name
		self.__health = 20
		self.__defense = 0
	def __str__(self):
		return '{}: {}'.format(self.getName(), self.getDescription())

	#Name the monster we are fighting
	#The description is printed at the start to give
	#additional details
	def getName(self):
		return self.__name

	def getDescription(self):
		return 'The Water Starter Pokemon'
	#Basic Attack Move
	#This will be the most common attack the monster makes
	#You are passed the monster you are fighting
	def basicAttack(self,enemy):
		print('{} used {} on {}'.format(self.getName(), self.basicName(), enemy.getName()))
		enemy.doDamage(2)
	#Print the name of the attack used
	def basicName(self):
		return 'Hydropump'

	#Defense Move
	#This move is used less frequently to
	#let the monster defend itself
	def defenseAttack(self,enemy):
		print('{} used {} on {}'.format(self.getName(), self.defenseName(), enemy.getName()))
		self.__defense -= 1

	#Print out the name of the attack used
	def defenseName(self):
		return 'Protect'

	#Special Attack
	#This move is used less frequently
	#but is the most powerful move the monster has
	def specialAttack(self,enemy):
		print('{} used {} on {}'.format(self.getName(), self.specialName(), enemy.getName()))
		enemy.doDamage(3)

	def specialName(self):
		return 'Hydro Cannon'

	#Health Management
	#A monster at health <= 0 is unconscious
	#This returns the current health level
	def getHealth(self):
		return self.__health

	#This function is used by the other monster to
	#either do damage (positive int) or heal (negative int)
	def doDamage(self,damage):
		self.__health -= damage + self.__defense
		self.__defense = 0

	#Reset Health for next match
	def resetHealth(self):
		self.__health = 20
