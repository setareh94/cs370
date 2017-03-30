# COMP 370, Spring 2017
# Program #2, DFA Simulation
# Co-Authored: Setareh Lotfi and Katie Levy

#System library for read and write
import sys
import os
from collections import defaultdict
from collections import deque
numberOfStates = 0
alphabets = []
transition = defaultdict()
acceptingStates = []
inputs = []


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
	print(x)
	alphabets = list((x.strip("\n")))

# Read through all the transitions
# and add them to the transition dictionary
# with the state and input as the key mapping to
# the resulting state
	m = f.readline()
	while( "'" in m):
		a,b,c = m.split("'")
		b = b.strip()
		c = c.strip(" ")
		if tuple((int(a),b)) in transition:
			transition[tuple((int(a),b))].append(c.strip("\n"))
		else:
			transition[tuple((int(a),b))] = list(c.strip("\n"))
		m = f.readline()
		
	m = f.readline()
	startState = m.strip("\n")

	acceptingStates = list((map(int, f.readline().split())))
	l = f.readline()
	while l:
		inputs.append(l.strip("\n"))
		l = f.readline()

def toDFA():
	DFATransitions = defaultdict()
	queue = deque()
	start = list(startState)
	if start not in queue:
		queue.append(start)
	while (len(queue)!=0):
		currentState = queue.popleft()
		nextStates = list()
		print(alphabets)
		for a in alphabets:
			for eachState in currentState:
				v = tuple((currentState, a))
				print(v)
				if v in transition:
					for x in transition[(tuple(currentState, a))]:
						nextStates.append(x)
			DFATransitions[tuple(currentState, a)] = nextStates
			if nextStates not in queue:
				queue.append(nextStates)
	print(DFATransitions)			





# Main function
if __name__ == '__main__':
	readFile(sys.argv[1])
	print(transition)
	print(startState)
	toDFA()