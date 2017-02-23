import sys
import os
from collections import defaultdict

numberOfStates = 0
alphabets = []
states = {} 
transition = {}
acceptingStates = []
inputs = []


global startState

def readFile(s):
	global startState
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
		transition[tuple((int(a),int(b)))] = c.strip("\n")
		m = f.readline()
	startState = int(m.strip("\n"))
	print("here %s",startState)

	acceptingStates = f.readline().split()
	l = f.readline()
	while l:
		inputs.append(l.strip("\n"))
		print(inputs)
		l = f.readline()

def DFA(inputs):
	currentState = startState

	for val in inputs:
		nextState = transition[tuple((int(currentState), int(val)))]
		currentState = nextState
		print(currentState)
	if currentState in acceptingStates:
		print("Accept")
		return
	print("Reject")

if __name__ == '__main__':
	readFile('dfa1.txt')
	print("Alphabet is %s \n transition %s \n inputs: %s " %(alphabets,transition,inputs))  

	print(states)
	print(transition)
	for i in inputs:
		DFA(i)




