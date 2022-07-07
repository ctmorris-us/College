#Mark Boady and Matthew Burlick
#Drexel University 2018
#CS 172

from monster import Dragon, Blastoise
import random

#This function has two monsters fight and returns the winner
def monster_battle(m1, m2):

	#first reset everyone's health!
	m1.resetHealth()
	m2.resetHealth()

	#next print out who is battling
	print("Starting Battle Between")
	print(m1)
	print(m2)

	#Whose turn is it?
	if random.randint(1,100) >= 50:
		attacker = m1
		defender = m2
	else:
		attacker = m2
		defender = m1

	#Select Randomly whether m1 or m2 is the initial attacker
	#to other is the initial definder
	######TODO######

	print(attacker.getName()+" goes first.\n")
	#Loop until either 1 is unconscious or timeout
	while( m1.getHealth() > 0 and m2.getHealth() > 0):
		#Determine what move the monster makes
		#Probabilities:
		#	60% chance of standard attack
		#	20% chance of defense move
		#	20% chance of special attack move

		#Pick a number between 1 and 100
		move = random.randint(1,100)
		#It will be nice for output to record the damage done
		before_health=defender.getHealth()

		#for each of these options, apply the appropriate attack and
		#print out who did what attack on whom
		if( move >=1 and move <= 60):
			#Attacker uses basic attack on defender
			attacker.basicAttack(defender)
		elif move>=61 and move <= 80:
			#Defend!
			attacker.defenseAttack(defender)
		else:
			#Special Attack!
			attacker.specialAttack(defender)

		#Print the names and healths after this round
		print('{} at {}'.format(m1.getName(), m1.getHealth()))
		print('{} at {}\n'.format(m2.getName(), m2.getHealth()))

		if attacker.getHealth() <= 0:
			return defender
		if defender.getHealth() <= 0:
			return attacker
		#Swap attacker and defender
		attacker, defender = defender, attacker
	#Return who won
	######TODO######

#----------------------------------------------------
if __name__=="__main__":
	#Every battle should be different, so we need to
	#start the random number generator somewhere "random".
	#With no input Python will set the seed

	random.seed(0)
	first = Dragon("Drogon")
	second = Blastoise("Blastoise")

	winner = monster_battle(first,second)

	#Print out who won
	print('{} is victorious!'.format(winner.getName()))
