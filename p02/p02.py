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
startStateAfterE = None
inputs = []
newDFATransition = {}
newStartState = None
newAcceptStates = []


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
	findNewStartState()
	start = list(startStateAfterE)
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
			nextStates = sorted(nextStates)

			DFATransitions[tuple((tuple(currentState,), a))] = nextStates

			if (sorted(nextStates) not in queue) and (sorted(nextStates) not in newStatesMarked) and sorted(nextStates):
				queue.append(sorted(nextStates))
	print(DFATransitions)
	
	changeStateNames(DFATransitions)

def findNewStartState():
	global startStateAfterE
	checkForE = deque()
	checkForE.append(startState)
	checkedForE = list()
	nextStates = list(startState)
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
	startStateAfterE = sorted(nextStates)


def changeStateNames(DFATransitions):

	lookup = {}
	i = 1
	global newDFATransition
	global newStartState
	global newAcceptStates
	for key, inp in DFATransitions:
		print("Printing lookup %s \n, key %s \n, input %s \n" %(lookup,key,inp))
		value = DFATransitions[key, inp]
		print(value)
		if key in lookup:
			print("inside if")
			print(key)
			newKey = tuple((lookup[key], inp))
		else:
			lookup[key] = i
			newKey = (tuple((i, inp)))
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
	newStartState = lookup[tuple(startStateAfterE,)]
	print(newStartState)
	for keys in lookup:
		print("printing keys")
		print(keys)
		for s in acceptingStates:
			if (str(s) in keys):
				print("hello")
				newAcceptStates.append(lookup[keys])
	print("new accepting states")
	print(newAcceptStates)



def readFileForInput(s):
	f = open(s, 'r')
	l = f.readline()
	while l:
		inputs.append(l.strip("\n"))
		l = f.readline()

# Run through the inputs based on the DFA created
# and output accept if the input is in the language
# or output reject if the input is not in the language
def DFAChecking():
	currentState = newStartState
	print("accepting states")
	print(acceptingStates)
	if (inputs) :
		print("printing inputs")
		print(inputs)
		for val in inputs:
			currentState = newStartState
			#empty strings should be accepted only if the accepting state was same as the current sate
			if len(val) == 0:
				if currentState in newAcceptStates:
				# print("accepting")
				# print(val)
					print("Accept")
				else:
					print("Reject")
			else:
				for i in val:
					reject = False
					try:
						nextState = newDFATransition[tuple((int(currentState), i))]
						currentState = int(nextState)
					except KeyError:
						reject = True

				if currentState in newAcceptStates and not reject:
					# print("accepting")
					# print(val)
					print("Accept")
				else:
					# print(val)
					print("Reject")

# Main function
if __name__ == '__main__':
	readFile(sys.argv[1])
	readFileForInput(sys.argv[2])	
	toDFA()
	DFAChecking()