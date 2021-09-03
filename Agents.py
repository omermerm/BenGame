import auxf
import random

# An agent in the world who is able to fight.
class Agent(object):
	
	def __init__(self, name, hp, attack, defense):
		self.name = name
		self.max_hp = hp
		self.hp = self.max_hp
		self.attack_val = attack
		self.defense_val = defense
	
	def __str__(self):
		return self.name
		
	def stats(self): #Print stats
		auxf.print_wait("{}\'s stats -- HP: {}/{}, ATK: {}, DEF: {}\n".format(self.name, self.hp, self.max_hp, self.attack_val, self.defense_val))
	
	def is_alive(self): #Check whether agent is alive
		return self.hp>0
	
	def take_blow(self, blow_strength): #Reduce HP by blowStrength-defense
		damage = max(0, blow_strength - self.defense_val)
		self.hp = max(0, self.hp - damage)
		if damage == 0:
			auxf.print_wait("{0} was able to block the attack completely and takes no damage!\n".format(self))
		else:
			auxf.print_wait("{0} takes {1} damage! {0} has {2} HP remaining.\n".format(self, damage, self.hp))
	
	def attack(self, enemy): #Hit another agent
		auxf.print_wait("{} swings at {}!".format(self,enemy))
		enemy.take_blow(auxf.rolld(self.attack_val))
	
	def take_action(self, enemy): #Method called when its the agent's turn in battle. Returns a boolean specifying whether the battle should be stopped.
		self.attack(enemy)
		stop_battle = False
		return stop_battle
		
	def at_full_health(self):
		return self.max_hp == self.hp
		
	def full_heal(self):
		self.hp = self.max_hp

class Player(Agent):

	actions_dictionary = {"attack" : "Attack", "a" : "Attack", "A" : "Attack", "Attack" : "Attack", "block" : "Block", "b" : "Block", "B" : "Block", "Block" : "Block", "escape" : "Escape", "e" : "Escape", "E" : "Escape", "Escape" : "Escape"}
	
	DIE_HP = 10
	DIE_ATK = 8
	DIE_DEF = 4
	
	def __init__(self, name):
		self.name = name
		self.max_hp = 5
		self.hp = self.max_hp
		self.attack_val = 4
		self.defense_val = 0
		self.level_up(False)
		
	def commit_seppuku(self): #Commit suicide
		auxf.print_wait("Realizing the futility of it all, {} blinks out of existence.\n".format(self))
		self.hp = 0
		
	def attempt_escape(self, enemy): #Invokes an escape attempt
		auxf.print_wait("{} is attempting to escape!\n".format(self))
		succeeded = random.randrange(2) == 1
		if succeeded:
			auxf.print_wait("{} succeeded in escaping {}! Hurray for cowardice!\n".format(self, enemy))
		else:
			auxf.print_wait("{} failed to escape {}!\n".format(self, enemy))
		return succeeded
		
	def take_action(self, enemy):
		stop_battle = False
		made_decision = False
		while(not made_decision):
			input_str = auxf.input_wait("What would you like to do? (A)ttack, (B)lock, (E)scape?\n")
			decision = Player.actions_dictionary.get(input_str)
			if decision == "Attack":
				made_decision = True
				self.attack(enemy)
			elif decision == "Escape":
				made_decision = True
				if self.attempt_escape(enemy):
					stop_battle = True
			elif decision == "Block":
				made_decision = True
				auxf.print_wait("Your turn was wasted on attempting to use an unimplemented command! Whoops!\n")
			else:
				auxf.print_wait("Invalid input.\n")
		return stop_battle
	
	def rest(self): #heals between 1 and 10% of max hp
		if self.at_full_health():
			auxf.print_wait("Being perfectly healthy, {} decides to skip a well-deserved rest.\n".format(self))
		else:
			ten_percent = self.max_hp // 10
			heal_amount = random.randrange(ten_percent) + 1
			actual_heal = min(heal_amount, self.max_hp - self.hp)
			self.hp += actual_heal
			if actual_heal == 1:
				auxf.print_wait("A short break from the action allows {} to regain {} health point\n".format(self, actual_heal))
			else:
				auxf.print_wait("A short break from the action allows {} to regain {} health points\n".format(self, actual_heal))
			
	def level_up(self,announce): #announce is a boolean value determining whether to announce the level up or do it silently
		max_hp_inc = auxf.rolld(Player.DIE_HP)
		atk_val_inc = auxf.rolld(Player.DIE_ATK)
		def_val_inc = auxf.rolld(Player.DIE_DEF)
		if announce:
			auxf.print_wait("{0} has levelled up! {0}'s HP increases by {1}! {0}'s ATK increases by {2}! {0}'s DEF increases by {3}!\n{0} is fully healed!".format(self,max_hp_inc,atk_val_inc,def_val_inc))
		self.max_hp += max_hp_inc
		self.attack_val += atk_val_inc
		self.defense_val += def_val_inc
		self.full_heal()
		
		

class Monster(Agent):

	monster_types = ["Slime"]
	slime_first_names = ["Oozy", "Slimey", "Blobbers", "Flipflop", "Puddle", "Molten", "Flow"]
	slime_last_names = ["McSlithers", "O'jello", "Sløpssøn", "Van Spritz", "Von Schlepzeug", "Ben Shlul", "Congellato"]
	
	monster_types_dictionary = {"Slime" : ((slime_first_names, slime_last_names),(10,4,4))}
	DICT_NAME = 0
	DICT_ATTRIBUTE_DICE = 1
	DIE_HP = 0
	DIE_ATK = 1
	DIE_DEF = 2
	
	def __init__(self, level = 1, species = auxf.random_select(monster_types)):
		self.species = species
		self.name = Monster.monster_name_generate(self.species)
		(self.max_hp, self.attack_val, self.defense_val) = Monster.monster_stats_generate(level, self.species)
		self.full_heal()
		
	def monster_stats_generate(level, species):
		dice = Monster.monster_types_dictionary[species][Monster.DICT_ATTRIBUTE_DICE]
		max_hp = auxf.rolld_times(dice[Monster.DIE_HP], level)
		atk_val = auxf.rolld_times(dice[Monster.DIE_ATK], level)
		def_val = auxf.rolld_times(dice[Monster.DIE_DEF], level)
		return (max_hp, atk_val, def_val)
		
	def monster_name_generate(species):
		(first_names, last_names) = Monster.monster_types_dictionary[species][Monster.DICT_NAME]
		first_name = auxf.random_select(first_names)
		last_name = auxf.random_select(last_names)
		name = first_name + ' ' + last_name
		return name
	
	def declare_presence(self):
		auxf.print_wait("A wild {} appears!".format(self.species))
		self.stats()
	
