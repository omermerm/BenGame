import auxf
import battle
from Agents import Player
from Agents import Monster

#setting up
playerName = auxf.input_wait("Type the name of your character:\n")
player = Player(playerName)

#turn start
while(player.is_alive()):
	player.stats()
	choice = auxf.input_wait("Would you like to fight?\n")
	if choice == "No":
		player.commit_seppuku()
	elif choice == "Yes": #fight monster
		enemy = Monster()
		enemy.declare_presence()
		while not battle.battle_round(player,enemy):
			auxf.wait()
		if player.is_alive():
			player.rest()
	else:
		auxf.print_wait(r"Please answer Yes/No." + "\n")
print("You seem to have died! Goodbye~!\n")