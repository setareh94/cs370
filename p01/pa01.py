import sys
import os
from collections import defaultdict

numberOfStates = 0
alphabets = []
transition = {}
acceptingStates = []
inputs = []


global startState

def readFile(s):
	global startState
	global acceptingStates
	f = open(s,'r')

	numberOfStates = f.readline()
	print(numberOfStates)
	x = f.readline()
	alphabets = list(x)
	m = f.readline()
	while( "'" in m):
		a,b,c = m.split("'")
		b = b.strip()
		c = c.strip(" ")
		transition[tuple((int(a),b))] = c.strip("\n")
		m = f.readline()
	startState = int(m.strip("\n"))

	acceptingStates = f.readline().split()
	l = f.readline()
	while l:
		inputs.append(l.strip("\n"))
		l = f.readline()

def DFA(inputs):
	currentState = startState

	for val in inputs:
		nextState = transition[tuple((int(currentState), val))]
		currentState = nextState
	if currentState in acceptingStates:
		print("Accept")
		return
	print("Reject")

if __name__ == '__main__':
	readFile(sys.argv[1])
	print("Alphabet is %s \n transition %s \n inputs: %s " %(alphabets,transition,inputs))
	for i in inputs:
		DFA(i)




