import sys
import os
from collections import defaultdict

numberOfStates = 0
alphabets = []
states = {} 
transition = defaultdict(set)
startState = 0
acceptingStates = []
inputs = []



def readFile(s):
	f = open(s,'r')

	numberOfStates = f.readline()
	print(numberOfStates)
	x = f.readline()
	alphabets = list(x)
	m = f.readline()
	while( "'" in m):
		a,b,c = m.split()
		b = b.split("'")
		transition[(a, b)] = c
		m = f.readline()
	startState = m
	acceptingStates = f.readline().split()
	l = f.readline()
	while l:
		inputs.add(m)
		l = f.readline()


if __name__ == '__main__':
	readFile('dfa1.txt')
	print("Alphabet is %s \n transition %s \n states are %s: \n inputs: %s \n" %(alphabets,transition,acceptingStates,inputs))  

	print(states)
	print(transition)




