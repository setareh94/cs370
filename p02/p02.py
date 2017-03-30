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
	newStatesMarked = list()
	queue = deque()
	start = list(startState)
	if start not in queue:
		queue.append(start)
	i = 0
	while (queue):
		currentState = queue.popleft()
		newStatesMarked.append(currentState)
		nextStates = list()
		for a in alphabets:
			nextStates = list()
			for eachState in currentState:
				v = tuple((int(eachState), a))
				if v in transition:
					for x in transition[v]:
						if x not in nextStates:
							nextStates.append(x)
			checkForE = deque()
			checkForE.append(nextStates + currentState)
			checkedForE = list()
			while (checkForE):
				curState = checkForE.popleft()
				for eachState in curState:
					if eachState not in sorted(checkedForE):
						checkedForE.append(eachState)
						v = tuple((int(eachState), "e"))
						if v in transition:
							for x in transition[v]:
								if x not in nextStates:
									nextStates.append(x)
									if (x not in sorted(checkForE)) and (x not in sorted(checkedForE)):
										checkForE.append(x)

			DFATransitions[tuple((tuple(currentState,), a))] = nextStates
			nextStates = sorted(nextStates)

			if (sorted(nextStates) not in queue) and (sorted(nextStates) not in newStatesMarked) and sorted(nextStates):
				queue.append(sorted(nextStates))
	print(DFATransitions)			


	lookup = {}
	i = 1
	newDFATransition = {}
	for key, inp in DFATransitions:
		print(lookup)
		print(key)
		print(inp)
		value = DFATransitions[key, inp]
		print(value)
		if key in lookup:
			print("inside if")
			print(key)
			newKey = tuple((lookup[key], inp))
		else:
			lookup[key] = i
			newKey = tuple((i, inp))
			i = i +1 
		if tuple(value,) in lookup:
			newValue = lookup[tuple(value,)]
		else:
			lookup[tuple(value,)] = i
			newValue = i
			i = i +1
		newDFATransition[newKey] = newValue
		print("printing new DFATRAns")
		print(newDFATransition)
	newStartState = lookup[tuple(startState,)]
	print(newStartState)


# Main function
if __name__ == '__main__':
	readFile(sys.argv[1])	
	toDFA()