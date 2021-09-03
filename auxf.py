from time import sleep
import random

def wait(): #delay
	sleep(0.5)

def input_wait(string): #Take input from user and then delay
	inp = input(string + " -")
	print_wait("")
	return inp

def print_wait(string): #Print a string, then wait
	print(string)
	wait()
	
def random_select(list):
	list_length = len(list)
	selection = random.randrange(list_length)
	return list[selection]
	
def rolld(d):
	return random_select(range(1,d+1))
	
def rolld_times(d,n):
	sum = 0
	for i in range(n):
		sum += rolld(d)
	return sum