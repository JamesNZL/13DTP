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

def player_information():
	playerName = ""

	while not playerName.isalpha():
		playerName = input("\nWhat is your name?: ").capitalize()

		if playerName.isalpha():
			break
		
		else:
			print("\nYour name must only contain letters A-Z.")

	print("\nWhich hero race would you like to select?\n")
	numbered_output(RACE_OPTIONS)
	playerRace = RACE_OPTIONS[user_input(len(RACE_OPTIONS), "your choice") - INDEX_OFFSET]

	print("\nWhich character class would you like your hero to be?\n")
	numbered_output(CHAR_CLASS_OPTIONS)
	playerCharClass = CHAR_CLASS_OPTIONS[user_input(len(CHAR_CLASS_OPTIONS), "your choice") - INDEX_OFFSET]

	print("\nWhich weapon would you like to use?\n")
	numbered_output(WEAPON_OPTIONS)
	playerWeapon = WEAPON_OPTIONS[user_input(len(WEAPON_OPTIONS), "your choice") - INDEX_OFFSET]

	return playerName, playerRace, playerCharClass, playerWeapon

def restart_or_exit():
	ACTION_OPTIONS = ("Start new game", "Exit program")
	print("\nWould you like to start a new game, or exit the program?\n")
	numbered_output(ACTION_OPTIONS)
	restartInput = user_input(len(ACTION_OPTIONS), "your choice")
	
	if ACTION_OPTIONS[restartInput - INDEX_OFFSET] == "Exit program":
		sys.exit()

	print("")

def battle():
	game.initiative = random.randint(INITIATIVE_MINIMUM, INITIATIVE_MAXIMUM)
	player.initiative = random.randint(INITIATIVE_MINIMUM, INITIATIVE_MAXIMUM)

	while player.initiative == game.initiative:
		player.initiative = random.randint(INITIATIVE_MINIMUM, INITIATIVE_MAXIMUM)

	if player.initiative > game.initiative:
		game.health, game.alive = attack(player.name, player.weapon, player.strength, game.enemy, game.health)

		if game.alive == True:
			player.health, player.alive = attack(game.enemy, game.weapon, game.strength, player.name, player.health)

	else:
		player.health, player.alive = attack(game.enemy, game.weapon, game.strength, player.name, player.health)

		if player.alive == True:
			game.health, game.alive = attack(player.name, player.weapon, player.strength, game.enemy, game.health)

def attack(attackerName, attackerWeapon, attackerStrength, opponentName, opponentHealth):
	roundHit = random.randint(0, 1)

	if roundHit == 0:
		print("\n{} has missed {} with their {}. They remain on {} HP.".format(attackerName.title(), opponentName, attackerWeapon, opponentHealth))

	else:
		opponentHealth -= attackerStrength

		print("\n{} has landed a hit with their {}, {} is now on {} HP.".format(attackerName.title(), attackerWeapon, opponentName, opponentHealth))

	if opponentHealth < 1:
		print("\n{} has successfully slain {} with their {}.".format(attackerName.title(), opponentName, attackerWeapon))

		return opponentHealth, False

	else:
		return opponentHealth, True

class Enemy:
	def __init__(self):
		self.enemy = random.choice(ENEMY_OPTIONS)
		self.weapon = random.choice(WEAPON_OPTIONS)
		self.health = random.randint(HEALTH_MINIMUM, HEALTH_MAXIMUM)
		self.strength = random.randint(STRENGTH_MINIMUM, STRENGTH_MAXIMUM)
		self.initiative = random.randint(INITIATIVE_MINIMUM, INITIATIVE_MAXIMUM)
		self.alive = True

class Hero:
	def __init__(self, name, race, charClass, weapon):
		self.name = name
		self.race = race
		self.Character_class = charClass
		self.weapon = weapon
		self.health = random.randint(HEALTH_MINIMUM, HEALTH_MAXIMUM) - RACE_HEALTH[race]

		if self.weapon == CHAR_CLASS_WEAPONS[self.Character_class]:
			strengthModifier = WEAPON_MODIFIER[self.weapon]

			print("\n{}s are highly proficient with a {}, your strength has increased by {}.".format(self.Character_class, self.weapon, strengthModifier))

		else:
			strengthModifier = 0

		self.strength = random.randint(STRENGTH_MINIMUM, STRENGTH_MAXIMUM) + strengthModifier
		self.initiative = random.randint(INITIATIVE_MINIMUM, INITIATIVE_MAXIMUM)
		self.alive = True

MINIMUM_INPUT = 1
RANGE_OFFSET = 1
INDEX_OFFSET = 1
INDEX_START = 0
ENUMERATE_START = 1
ENEMY_OPTIONS = ["the Roman", "the Parthian", "the Celt", "the Gaul", "the Spartan", "the Egyptian"]
WEAPON_OPTIONS = ["Two Handed Sword" , "Dagger", "Holy Cross", "Short Sword", "Dart", "Fighting Shield", "Double Daggers", "Long Bow", "Magic Staff", "Wand"]
RACE_OPTIONS = ["Human", "Dwarf", "Halfling", "Elf", "Gnome", "Half-Orc", "Half-Elf"]
RACE_HEALTH = {
	"Human": 0,
	"Dwarf": 3,
	"Halfling": -3,
	"Elf": 2,
	"Gnome": -3,
	"Half-Orc": 5,
	"Half-Elf": 2
	}
CHAR_CLASS_OPTIONS = ["Barbarian", "Bard", "Cleric", "Fighter", "Druid", "Paladin", "Rogue", "Ranger", "Sorcerer" , "Wizard"]
CHAR_CLASS_WEAPONS = {
	"Barbarian": "Two handed sword",
	"Bard": "Dagger",
	"Cleric": "Holy Cross",
	"Fighter": "Short Sword",
	"Druid": "Dart",
	"Paladin": "Fighting Shield",
	"Rogue": "Double Daggers",
	"Ranger": "Long Bow",
	"Sorcerer": "Magic Staff",
	"Wizard": "Wand"
}
WEAPON_MODIFIER = {
	"Two Handed Sword": 5,
	"Dagger": 3,
	"Holy Cross": 1,
	"Short Sword": 1,
	"Dart": 3,
	"Fighting Shield": 4,
	"Double Daggers": 4,
	"Long Bow": 3,
	"Magic Staff": 2,
	"Wand": 5
}
HEALTH_MINIMUM = 50
HEALTH_MAXIMUM = 100
STRENGTH_MINIMUM = 10
STRENGTH_MAXIMUM = 25
INITIATIVE_MINIMUM = 1
INITIATIVE_MAXIMUM = 10

while True:
	print("Welcome to The Battle!")

	playerName, playerRace, playerCharClass, playerWeapon = player_information()

	player = Hero(playerName, playerRace, playerCharClass, playerWeapon)

	game = Enemy()

	battle()

	while game.alive == True and player.alive == True:
		ATTACK_OPTIONS = ("Attack again", "No")
		print("\nWould you like to attack again?\n")
		numbered_output(ATTACK_OPTIONS)
		attackInput = user_input(len(ATTACK_OPTIONS), "your choice")

		if ATTACK_OPTIONS[attackInput - INDEX_OFFSET] == "Attack again":
			battle()

		else:
			break

	if game.alive == False:
		print("\nCongratulations, {} has won the game!".format(player.name))

	elif player.alive == False:
		print("\nBetter luck next time, {} has been slain by {}.".format(player.name, game.enemy))

	restart_or_exit()