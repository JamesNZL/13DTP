import sys, random

def user_input(rangeMaximum, promptWord):
    inputValue = ""

    while inputValue not in range(MINIMUM_INPUT, rangeMaximum + RANGE_OFFSET):
        try:
            inputValue = int(input("\nEnter {}: ".format(promptWord)))

            if inputValue not in range(MINIMUM_INPUT, rangeMaximum + RANGE_OFFSET):
                print("\n{} must be between {} and {}.".format(promptWord.capitalize(), MINIMUM_INPUT, rangeMaximum))

        except:
            print("\n{} must be an integer between {} and {}.".format(promptWord.capitalize(), MINIMUM_INPUT, rangeMaximum))

    return inputValue

def numbered_output(dataStructure):
    for number, item in enumerate(dataStructure, ENUMERATE_START):
        print("{}) {}".format(number, item))

def restart_or_exit():
	ACTION_OPTIONS = ("Start new game", "Exit program")
	print("\nWould you like to start a new game, or exit the program?\n")
	numbered_output(ACTION_OPTIONS)
	restartInput = user_input(len(ACTION_OPTIONS), "your choice")
    
	if ACTION_OPTIONS[restartInput - INDEX_OFFSET] == "Exit program":
		sys.exit()

class Enemy:
	def __init__(self):
		self.enemy = random.choice(["Roman", "Parthian", "Celt", "Gaul"])
		self.weapon = random.choice(["Sword", "Axe", "Bow & Arrow", "Slingshot"])
		self.health = random.randint(50, 100)
		self.strength = random.randint(10, 25)
		self.alive = True

	def battle(self):
		heroStrength = random.randint(15, 30)

		heroHit = random.randint(0, 1)

		if heroHit == 0:
			print("\nYou have missed the {}! They remain on {} HP.".format(self.enemy, self.health))

		else:
			self.health -= heroStrength

			print("\nYou have dealt a blow, the {} is now on {} HP.".format(self.enemy, self.health))

		if self.health < 1:
			self.alive = False

			print("\nYou have successfully slain the {}.".format(self.enemy))

MINIMUM_INPUT = 1
RANGE_OFFSET = 1
INDEX_OFFSET = 1
INDEX_START = 0
ENUMERATE_START = 1

while True:
	print("Welcome to The Battle!")

	game = Enemy()

	game.battle()

	while game.alive == True:
		ATTACK_OPTIONS = ("Attack again", "No")
		print("\nWould you like to attack again?\n")
		numbered_output(ATTACK_OPTIONS)
		attackInput = user_input(len(ATTACK_OPTIONS), "your choice")

		if ATTACK_OPTIONS[attackInput - INDEX_OFFSET] == "Attack again":
			game.battle()

		else:
			print("\nStarting new game...")

			game = Enemy()

	print("\nCongratulations, you have won the game!")

	restart_or_exit()