# COMP 370, Spring 2017
# Program #1, DFA Simulation
# Co-Authored: Setareh Lotfi and Katie Levy

#System library for read and write
import sys
import os

numberOfStates = 0
alphabets = []
transition = {}
acceptingStates = []
inputs = []
regularExpressionList = []


global startState

# Open a file, s, and parse through the file to
# properly assign global variables for the DFA
def readFile(s):
	global startState
	global acceptingStates
	global alphabets
	f = open(s,'r')

	numberOfStates = f.readline()
	x = f.readline()
	alphabets = x.split()

# Read through all the transitions
# and add them to the transition dictionary
# with the state and input as the key mapping to
# the resulting state
	m = f.readline()

	while m:
		regularExpressionList.append(m.strip("\n"))
		m = f.readline()
	print(regularExpressionList)

# Run through the inputs based on the DFA created
# and output accept if the input is in the language
# or output reject if the input is not in the language
def DFA(inputs):
	currentState = startState
	if (inputs) :
		for val in inputs:
			nextState = transition[tuple((int(currentState), val))]

			currentState = int(nextState)

#empty strings should be accepted only if the accepting state was same as the current sate
	if len(inputs) == 0 and currentState in acceptingStates:
		print("Accept")
	else:
		if currentState in acceptingStates:
			print("Accept")
		else:
			print("Reject")

# Main function
if __name__ == '__main__':
	readFile(sys.argv[1])
	for i in inputs:
		DFA(i)



