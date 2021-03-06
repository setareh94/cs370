"""
 COMP 370, Spring 2017
 Program #3, Searching text for string that are 
 in the language of a regular expression
 Co-Authored: Setareh Lotfi and Katie Levy
"""

#System library for read and write
import sys
import os
#Python library for dictionary and queue
from collections import defaultdict
from collections import deque


""""""""""""""""""""""""""""""""""""""""""""""""
#				G E N E R A L
""""""""""""""""""""""""""""""""""""""""""""""""
# Global variables for easier transitons
numberOfStates = 0
alphabets = []          # List of alphabets
transition = defaultdict() 
transition_NFA = defaultdict
acceptingStates = set()	# List of accepting states
inputs = [] 			# List of DFA Inputs
startStateAfterE = None # Start state after epsilon transition
newDFATransition = {}   # Map for DFA transition
newStartState = None    # new start state for DFA
newAcceptStates = set() #set of accepting states
newStatesMarked = list()#New states that were visted
root = None 			#tree root
stateNumber = 0
finalNFA = None
startState = None
resultFile = None 		# file to write to



concatedExpressionList = [] #list of input concated

"""
Function: readFile
Arguments: fileName
Description:
	Open the file, fileName, and parse through the file to
	properly assign global variables for the NFA to 
	DFA conversion
"""
def readFile(fileName):

	global alphabets
	global inputs

	with open(fileName,'r') as f:

		x = f.readline()
		alphabets = list((x.strip("\n")))

		# Read in the Regular Expression
		m = f.readline()
		m = m.replace(" ", "")
		m = m.strip("\n")
		makeConcatToAppear(m)

		# Create syntax tree

		# setUpTheNodesInTree(m.strip("\n"))
		m = f.readline()

		# Read in the inputs
		while m:
			# setUpTheNodesInTree(m.strip("\n"))

			inputs.append(m.strip("\n"))
			m = f.readline()


"""
Class: NFAObject
Arguments: None
Description:
	An object to represent an NFA
"""

class NFAObject:

	states = list()
	accept = list()
	def __init__(self, start, states, accept, transition):
		self.start = start
		self.states = states
		self.accept = accept
		self.transition = transition

"""
Class: Node
Arguments: None
Description:
	Setting up the tree
	Nodes to represent tree nodes in the syntax tree
	Note: * operator only has a left child
"""
class Node:

	def __init__(self, value, left=None, right=None):
		self.value = value
		self.left = left
		self.right = right
	def __str__(self):
		return str(self.value)

""""""""""""""""""""""""""""""""""""""""""""""""
#	C O N V E R T  F R O M  NFA TO DFA
""""""""""""""""""""""""""""""""""""""""""""""""

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
	global newStatesMarked
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
			if currentState:
				for eachState in currentState:
					v = tuple((int(eachState), a))
					if v in transition_NFA:
						for x in transition_NFA[v]:
							if x not in nextStates:
								nextStates.append(x)
				# Check what state the next states could be in 
				# with the episilon transitions
				epsilonTransition(nextStates, currentState)
				# Add to the new transition function
				nextStates = sorted(nextStates)
			else:
				nextStates = currentState	

			DFATransitions[tuple((tuple(currentState,), a))] = nextStates

			if ((sorted(nextStates) not in queue) 
				and (sorted(nextStates) not in newStatesMarked)):
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
	checkForE.append(nextStates)
	checkedForE = list()

	while (checkForE):
		curState = checkForE.popleft()
		for eachState in curState:
			if eachState not in sorted(checkedForE):
				checkedForE.append(eachState)
				v = tuple((int(eachState), "e"))
				if v in transition_NFA:
					mult = transition_NFA[v]
					for x in mult:
						# Check if multiple epsilon transitions from the state
						if type(x) is list:
							for y in x:
								if y not in nextStates:
									nextStates.append(y)
									if (x not in sorted(checkForE)) and (y not in sorted(checkedForE)):
										checkForE.append(y)
						else:
							if x not in nextStates:
								nextStates.append(x)
								if (x not in sorted(checkForE)) and (x not in sorted(checkedForE)):
									checkForE.append([x])
	
						


"""
Function: findNewStartState
Arguments: none
Description:
	Find the new start state compensating
	for epsilon transitions
"""
def findNewStartState():

	global startStateAfterE
	global startState
	checkForE = deque()
	checkForE.append(startState)
	checkedForE = list()
	nextStates = list()
	nextStates.extend(startState)

	while (checkForE):
		curState = checkForE.popleft()

		for eachState in curState:
			eachState = int(eachState)

			if eachState not in sorted(checkedForE):
				checkedForE.append(eachState)
				# search for any epsilon transitions
				v = tuple((int(eachState), "e"))
				if v in transition_NFA:
					mult = transition_NFA[v]
					for x in mult:
						# Check if multiple epsilon transitions from the state
						if type(x) is list:
							for y in x:
								if y not in nextStates:
									nextStates.append(y)
									if (x not in sorted(checkForE)) and (y not in sorted(checkedForE)):
										checkForE.append(y)
						else:
							if x not in nextStates:
								nextStates.append(int(x))
								if (x not in sorted(checkForE)) and (x not in sorted(checkedForE)):
									checkForE.append([x])
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
		# key is a current state in the NFA
		if key in lookup:
			newKey = tuple((lookup[key], inp))
		else:
			lookup[key] = i
			newKey = (tuple((i, inp)))
			i = i +1 
		# value is a next state in the NFA
		if tuple(value,) in lookup:
			newValue = lookup[tuple(value,)]
		else:
			lookup[tuple(value,)] = i
			newValue = i
			i = i +1
		newDFATransition[newKey] = newValue

	newStartState = lookup[tuple(startStateAfterE,)]
	# lookup new accept states
	for keys in lookup:
		for s in acceptingStates:
			if (s in keys):
				newAcceptStates.add(lookup[keys])




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#	C H E C K   IF  I N P U T  IS  A C C E P T T E D  BY  DFA
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""
Function: checkDFAInput
Arguments: None
Description:
	Run the DFA through the input given in the file
	write to another file with true for inputs in the regular expression
	and write false for inputs not in the regular expression
"""
def checkDFAInput():

	currentState = newStartState

	if (inputs) :
		with open(resultFile, 'w') as f:

			for val in inputs:
				currentState = newStartState
				#empty strings should be accepted only
				# if the accepting state was same as the current sate
				if len(val) == 0:
					if currentState in newAcceptStates:
						f.write("true\n")
					else:
						f.write("false\n")

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
						f.write("true\n")

					else:
						f.write("false\n")



""""""""""""""""""""""""""""""""""""""""""""""""
#	C O N V E R T  F R O M  REGEX TO NFA
""""""""""""""""""""""""""""""""""""""""""""""""

"""
Function: print_tree
Arguments: the root node of the tree
Description:
	Function to print the values in the syntax tree
"""
def print_tree(node, level=0):

	if node == None: return
	print('\t' * level + node.value)
	print_tree(node.left, level + 1)
	print_tree(node.right, level + 1)

"""
Function: setUpTheNodesInTree
Arguments: string expression of the regualr expression
Description:
	Parse the regular expression to create a syntax tree
"""
def setUpTheNodesInTree(expression):

	global root
	operatorStack = []
	operandsStack = []
	for i in expression:		
		# Check if symbol from the alphabet
		if(i in alphabets or i == 'e'):
			x = Node(i)
			operandsStack.append(x)
		elif i == '(':
			operatorStack.append(i)
		elif(i == ')'):
			# pop operators off stack until ( is popped off
			v = operatorStack.pop()
			while (v != '(' and len(operatorStack) > 0):
				# create new syntax tree and add it to operands stack
				createNewSyntaxTree(v, operandsStack, operatorStack)
				v = operatorStack.pop()
			if (v != '(' and len(operatorStack) == 0):
				with open(resultFile, 'w') as f:
					f.write("Invalid expression\n")
					exit()
		# Check if an operator
		elif(i in processingActions and i != 'e'):
			cont = True
			while(cont):
				if(len(operatorStack) > 0):
					op = operatorStack.pop()
					# check if op has a greater than or equal precedence to operator just scanned
					# precedence is star highest, then concatenation, then union
					if((op == '*') | (op == '`' and i == '|') | (op == '`' and i != '*') | (op == '|' and i == '|')):
						# op >= i
						# create new syntax tree and add it to operands stack
						createNewSyntaxTree(op, operandsStack, operatorStack)
						# push operand just scanned onto stack
						#operatorStack.append(i)
					else:
						# op < i
						# push op back onto the operator stack and i
						operatorStack.append(op)
						operatorStack.append(i)
						cont = False
				else:
					# operator stack is empty
					operatorStack.append(i)
					cont = False
		else:
				#invalid expression throw error
			with open(resultFile, 'w') as f:
				f.write("Invalid expression\n")			
				exit()
	# There are no more characters to scan
	# Empty the operator stack and create new syntax tree for each operator
	while(len(operatorStack) > 0):
		op = operatorStack.pop()
		createNewSyntaxTree(op, operandsStack, operatorStack)
	# Pop the root of the syntax tree off the operand stack
	root = operandsStack.pop()


"""
Function: createNewSyntaxTree
Arguments: operation type, operand stack, operator stack
Description:
	Creates a new syntax tree from operandsStack depending on operation
	and adds it back onto the operands stack
"""
def createNewSyntaxTree(op, operandsStack, operatorStack):
	# Create syntax tree node from op
	with open(resultFile, 'w') as f:
		if(op == '*'):
			if(len(operandsStack) == 0):
				f.write("Invalid expression\n")
				exit()
			left = operandsStack.pop()
			x = Node(op, left)
		else:
			if(len(operandsStack) == 0):
				f.write("Invalid expression\n")
				exit()
			right = operandsStack.pop()
			if(len(operandsStack) == 0):
				f.write("Invalid expression\n")
				exit()
			left = operandsStack.pop()
			x = Node(op, left, right)
		# push new syntax tree onto operands stack
		operandsStack.append(x)



"""
Function: helperSyntaxTreeToNFA
Arguments: Node object of the root of the syntax tree
Description:
	Call syntaxTreeToNFA recursively to create an NFA from 
	the syntax tree of the regex.
	The global variables startState, finalNFA, and transition_NFA
	should be set.
"""
def helperSyntaxTreeToNFA(val):

	global startState
	global finalNFA
	global transition_NFA
	finalNFA = syntaxTreeToNFA(val)
	startState = finalNFA.start
	acceptingStates.update(finalNFA.accept)
	numberOfStates = len(finalNFA.states)
	transition_NFA = finalNFA.transition
	transition_NFA = dict((k,v) for k,v in transition_NFA.items())

"""
Function: syntaxTreeToNFA
Arguments: Node object of a piece of the syntax tree
Description:
	A recursive function to create NFA's for each operation in the 
	input Node.
"""
def syntaxTreeToNFA(val):

	global stateNumber
	current = val.value
	if (current in alphabets):
		states = list()
		states.append(stateNumber)
		states.append(stateNumber + 1)
		trans = defaultdict()
		trans[tuple((stateNumber, current))] = [stateNumber + 1]
		accept = list()
		accept.append(stateNumber + 1)
		start = [stateNumber]
		stateNumber = stateNumber + 2
		return NFAObject(start, states, accept, trans )
	elif (current == 'e'):
		return epsilon()
	elif (current == 'N'):
		return emptySet()
	elif (current == '*'):
		if val.left:
			left = syntaxTreeToNFA(val.left)
		return star(left)
	elif (current == '`'):
		if val.left:
			left = syntaxTreeToNFA(val.left)
		if val.right:
			right = syntaxTreeToNFA(val.right)

		return concat(left, right)
	elif (current == '|'):
		if val.left:
			left = syntaxTreeToNFA(val.left)
		if val.right:
			right = syntaxTreeToNFA(val.right)
		return union(left, right)

""""""""""""""""""""""""""""""""""""""""""""""""
#	S Y N T A X   T R E E   O P E R A T I O N S
""""""""""""""""""""""""""""""""""""""""""""""""
"""
Function: epsilon
Arguments: None
Description:
	Create an NFAObject object for the epsilon regex
"""
def epsilon():

	global stateNumber
	states = list()
	states.append(stateNumber)
	states.append(stateNumber + 1)
	trans = defaultdict()
	trans[tuple((stateNumber, 'e'))] = [stateNumber + 1]	
	accept = list()
	accept.append(stateNumber + 1)
	start = [stateNumber]
	stateNumber = stateNumber + 2
	return NFAObject(start, states, accept, trans )
"""
Function: emptySet
Arguments: None
Description:
	Create an NFAObject object for the emptySet regex
"""
def emptySet():

	states = list()
	states.append(stateNumber)
	trans = defaultdict()
	accept = list()
	start = [stateNumber]
	stateNumber = stateNumber + 1
	return NFAObject(start, states, accept, trans )

"""
Function: union
Arguments: left and right NFAObjects that will be unioned
Description:
	Create an NFAObject object for the union regex
"""
def union(left, right):

	global stateNumber
	newStart = stateNumber
	newStates = right.states + left.states
	newStates.append(newStart)
	transition = defaultdict()
	transition[tuple((newStart, 'e'))] = right.start + left.start
	transition.update(right.transition)
	transition.update(left.transition)
	accept = right.accept + left.accept
	stateNumber = stateNumber + 1
	return NFAObject([newStart], newStates, accept, transition)

"""
Function: star
Arguments: An NFAObject that will be starred
Description:
	Create an NFAObject object for the star regex
"""
def star(left):

	global stateNumber
	newStart = stateNumber
	newStates = left.states
	newStates.append(newStart)
	transition = defaultdict()
	transition[tuple((newStart, 'e'))] = left.start
	transition.update(left.transition)
	for accept in left.accept:
		transition[tuple((accept, 'e'))] = left.start
	accept = left.accept
	accept.append(newStart)
	stateNumber = stateNumber + 1
	return NFAObject([newStart], newStates, accept, transition)

"""
Function: concat
Arguments: left and right NFAObjects that will be concatenated together
Description:
	Create an NFAObject object for the concat regex
"""
def concat(left, right):

	newStart = left.start
	newStates = right.states + left.states
	left.transition.update(right.transition)
	transition = defaultdict()
	transition = left.transition
	for accept in left.accept:
		if((accept, 'e') in transition):
			transition[tuple((accept, 'e'))] = right.start + transition[tuple((accept, 'e'))]
		else:
			transition[tuple((accept, 'e'))] = right.start
	accept = right.accept
	return NFAObject(newStart, newStates, accept, transition)



 # Dictionary of all the actions available
processingActions = { 
	'e': epsilon,
	'N': emptySet,
	'|': union,
	'*': star,
	'`':concat,
}

"""
Function: makeConcatToAppear
Arguments: String expression
Description:
	Make the concatination shown for ace of putting it in the tree
"""
def makeConcatToAppear(expression):

	concatExp = ''

	if (len(expression)>1):
		for i in range(len(expression)-1):
			currentChar = expression[i]
			nextChar = expression[i+1]

			#Have if statment to check for epsilon and empty expressions
			if not currentChar and not nextChar:
				#I am not sure what should happen if we scan a empty expression 
				break
			if ((currentChar == ')' or currentChar == '*' or ((currentChar not in processingActions) and currentChar != '('))
	            and (nextChar == '(' or ((nextChar not in processingActions) and nextChar != ')'))):
				concatExp += currentChar + '`'
			else:
				concatExp +=currentChar

		fullyConcat =  concatExp + expression[len(expression)-1]
		concatedExpressionList.append(fullyConcat)
	else:
		concatedExpressionList.append(expression)


if __name__ == '__main__':

	if len(sys.argv) < 3:
		print ("Usage: \nArgument 1: Regex text file (e.g: re1In.txt) \n"
					+ "Argument 2: Desired file name to write the results to (e.g: DFA1_result.txt)\n" )
	else:
		readFile(sys.argv[1])
		resultFile = sys.argv[2]
		for regex in concatedExpressionList:
			setUpTheNodesInTree(regex)
		helperSyntaxTreeToNFA(root)
		conversionToDFA()
		checkDFAInput()
