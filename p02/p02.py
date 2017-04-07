# COMP 370, Spring 2017
# Program #2, DFA Simulation
# Co-Authored: Setareh Lotfi and Katie Levy

#System library for read and write
import sys
import os
#Python library for dictionary and queue
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
newAcceptStates = set()

global startState

# Open a file, s, and parse through the file to
# properly assign global variables for the NFA to 
# DFA conversion

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
			transition[tuple((int(a),b))] = [c.strip("\n")]
		m = f.readline()

		
	m = f.readline()
	#Store StartState from the file
	startState = m.strip("\n")

	#Store acceptionStates
	acceptingStates = list((map(int, f.readline().split())))

def conversionToDFA():
	print("Transtion is %s \n" % transition)
	DFATransitions = defaultdict()
	newStatesMarked = list()
	queue = deque()
	findNewStartState()
	start = list(startStateAfterE)
	if start not in queue:
		queue.append(start)
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
	print("Printing DFA Transitions")
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
		print("\n Printing lookup\n %s \n key %s \n, \n input %s \n" %(lookup,key,inp))
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
		print("printing new DFA Transition")
		print(newDFATransition)
	newStartState = lookup[tuple(startStateAfterE,)]
	print(newStartState)
	for keys in lookup:
		for s in acceptingStates:
			if (str(s) in keys):
				newAcceptStates.add(lookup[keys])
	print("new accepting states")
	print(newAcceptStates)


#Read the DFAinput files and store them for output
def readFileForDFAInput(s):
	file = open(s, 'r')
	nextLine = file.readline()
	while nextLine:
		inputs.append(nextLine.strip("\n"))
		nextLine = file.readline()

# Run through the inputs based on the DFA created
# and output accept if the input is in the language
# or output reject if the input is not in the language
def checkDFAInput():
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
					print("Accept")
				else:
					print("Reject")

# Main function
if __name__ == '__main__':
	readFile(sys.argv[1])
	readFileForDFAInput(sys.argv[2])	
	conversionToDFA()
	checkDFAInput()