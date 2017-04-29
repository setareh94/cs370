"""
 COMP 370, Spring 2017
 Program #2, NFA to DFA Conversion
 Co-Authored: Setareh Lotfi and Katie Levy
"""

#System library for read and write
import sys
import os
#Python library for dictionary and queue
from collections import defaultdict
from collections import deque

# Global variables for easier transitons
numberOfStates = 0
alphabets = []          # List of alphabets
transition = defaultdict() 
acceptingStates = []	# List of accepting states
inputs = [] 			# List of DFA Inputs
startStateAfterE = None # Start state after epsilon transition
newDFATransition = {}   # Map for DFA transition
newStartState = None    # new start state for DFA
newAcceptStates = set() #set of accepting states


"""
Function: readFile
Arguments: fileName
Description:
	Open the file, fileName, and parse through the file to
	properly assign global variables for the NFA to 
	DFA conversion
"""
def readFile(fileName):

	global startState
	global acceptingStates
	global alphabets
	global numberOfStates

	with open(fileName,'r') as f:

		numberOfStates = (f.readline()).strip("\n")
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


"""
Function: conversionToDFA
Arguments: none
Description:
	Convert the NFA to a DFA with a
	new transition function and new states
	keeping track of what states the NFA would be at
"""
def conversionToDFA():
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
			# Check what state the next states could be in 
			# with the episilon transitions
			epsilonTransition(nextStates, currentState)
			# Add to the new transition function
			nextStates = sorted(nextStates)
			DFATransitions[tuple((tuple(currentState,), a))] = nextStates

			if ((sorted(nextStates) not in queue) 
				and (sorted(nextStates) not in newStatesMarked)
				and sorted(nextStates)):
				queue.append(sorted(nextStates))
	#Covert from set of one states to set of integers
	changeStateNames(DFATransitions)


"""
Function: epsilonTransition
Arguments: nextstates, currentState
Description:
 	The function Check what state the next states could be in 
	with the episilon transitions
"""
def epsilonTransition(nextStates, currentState):
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


"""
Function: findNewStartState
Arguments: none
Description:
	Find the new start state compensating
	for epsilon transitions
"""
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


"""
Function: changeStateNames
Arguments: DFATransitions
Description:
	Takes in a dictionary containing DFA transition 
	functions (DFATransitions) and Convert DFA states 
	from the form of set of states to just one integer.
"""
def changeStateNames(DFATransitions):
	lookup = {}
	i = 1
	global newDFATransition
	global newStartState
	global newAcceptStates
	# Go through every transition states
	for key, inp in DFATransitions:
		value = DFATransitions[key, inp]
		if key in lookup:
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

	newStartState = lookup[tuple(startStateAfterE,)]

	for keys in lookup:
		for s in acceptingStates:
			if (str(s) in keys):
				newAcceptStates.add(lookup[keys])


"""
 Function: writeDFAtoFile
 Arguments: fileName
 Description:
	Takes in filename and write the created dfa 
	into a user specific file.
"""

def writeDFAtoFile(filename):
	with open(filename, 'w') as f:
		f.write(str(numberOfStates) + '\n')
		f.write("".join(i for i in alphabets) + '\n')
		result = "\n".join(str(key[0]) + " '" + key[1] + "' " + str(value) 
							for key, value in newDFATransition.items())
		f.write(result + '\n')
		f.write(str(newStartState) + '\n')
		f.write(" ".join(str(i) for i in newAcceptStates))


"""
 Function: readFileForDFAInput
 Arguments: fileName
 Description:
	Takes in filename and read the DFAinput files 
	and store them for output.
"""
def readFileForDFAInput(fileName):
	with open(fileName, 'r') as file:
		nextLine = file.readline()
		while nextLine:
			inputs.append(nextLine.strip("\n"))
			nextLine = file.readline()
 

"""
 Function: checkDFAInput
 Arguments: none
 Description:
	Run through the inputs based on the DFA created
	and prints accept if the input is in the language
	otherwise prints reject if the input is not in
	the language.
"""
def checkDFAInput():
	currentState = newStartState

	if (inputs) :
		for val in inputs:
			currentState = newStartState
			#empty strings should be accepted only
			# if the accepting state was same as the current sate
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
					#If the transition path did not exist reject
					except KeyError:
						reject = True

				if currentState in newAcceptStates and not reject:
					print("Accept")
				else:
					print("Reject")


"""
Main function
"""
if __name__ == '__main__':
	# Guide the user on the program usage
	if len(sys.argv) == 4:
		print ("Usage: \nArgument 1: NFA text file (e.g: NFA1.txt) \n"
				+ "Argument 2: Desired file name to write the equivalent DFA to (e.g: DFA1.txt)\n" + 
				"Argument 3: DFA input file to evaluate the produced DFA (e.g: DFAinput.txt)")
		readFile(sys.argv[1])
		#Third argument takes in DFAinput text file
		readFileForDFAInput(sys.argv[3])
		conversionToDFA()
		checkDFAInput()
		#Second argument takes in file name to output produced DFA 
		writeDFAtoFile(sys.argv[2])

	else:
		#First argument takes in NFA text file
		readFile(sys.argv[1])
		conversionToDFA()
		#Second argument takes in file name to output produced DFA 
		writeDFAtoFile(sys.argv[2])
