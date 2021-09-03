from Agents import Player
from Agents import Monster
import random
import auxf

#Perform a battle round. The attacker attacks once. The defender retaliates if it is still alive. The function returns whether the battle is over (someone died) as a boolean value.
def battle_round(attacker, defender):
	stop_battle = False
	if not stop_battle:
		stop_battle = attacker.take_action(defender)
	if not stop_battle:
		stop_battle = is_battle_decided(attacker, defender)
	if not stop_battle:
		stop_battle = defender.take_action(attacker)
	if not stop_battle:
		stop_battle = is_battle_decided(attacker, defender)
	return stop_battle

#Tests whether one of the fighters was defeated. If one of the fighters was defeated, prints this information to screen.
def is_battle_decided(fighter1, fighter2):
	battle_over = False
	if not fighter1.is_alive():
		auxf.print_wait("{0} is dead! {1} has defeated {0}!\n".format(fighter1, fighter2))
		battle_over = True
	elif not fighter2.is_alive():
		auxf.print_wait("{1} is dead! {0} has defeated {1}!\n".format(fighter1, fighter2))
		battle_over = True
	return battle_over
	