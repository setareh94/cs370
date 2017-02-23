import sys
import os
from collections import defaultdict

numberOfStates = 0
alphabets = []
states = {} 
transition = {}
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
		a,b,c = m.split("'")
		b = b.strip()
		transition[tuple((a,b))] = c
		m = f.readline()
	startState = m
	acceptingStates = f.readline().split()
	l = f.readline()
	while l:
		inputs.append(l.strip("\n"))
		print(inputs)
		l = f.readline()

def DFA(input):
	currentState = startState
	for val in input:
		nextState = transition[tuple((currentState, val))]
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




