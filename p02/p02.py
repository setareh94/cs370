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
	print("length is %d" % len(queue))
	print(queue)
	start = list(startState)
	if start not in queue:
		queue.append(start)
	print(queue)
	while (queue):
		currentState = queue.popleft()
		print(queue)
		nextStates = list()
		for a in alphabets:
			print("alphavet is")
			print(a)
			nextStates = list()
			for eachState in currentState:
				v = tuple((int(eachState), a))
				print("qeue is")
				print(queue)
				print("dsds")
				print(v)
				print(transition)
				if v in transition:
					for x in transition[v]:
						print("what is in next state")
						print(x)
						print(nextStates)
						if x not in nextStates:
							nextStates.append(x)
			DFATransitions[v] = nextStates
			print(DFATransitions)			
			print("before if")
			print(sorted(nextStates))
			nextStates = sorted(nextStates)

			if (sorted(nextStates) not in queue) and sorted(nextStates):
				queue.append(sorted(nextStates))
				print("after append")
				print(queue)
	print(DFATransitions)			





# Main function
if __name__ == '__main__':
	readFile(sys.argv[1])
	print(transition)
	print(startState)
	toDFA()