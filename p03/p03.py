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
transition_NFA = defaultdict
acceptingStates = set()	# List of accepting states
inputs = [] 			# List of DFA Inputs
startStateAfterE = None # Start state after epsilon transition
newDFATransition = {}   # Map for DFA transition
newStartState = None    # new start state for DFA
newAcceptStates = set() #set of accepting states
newStatesMarked = list()
stringsList = []
root = None
stateNumber = 0
finalNFA = None
startState = None
resultFile = None
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
	#print("pritning queue")
	#print(queue)
	#print(len(queue))
	while (queue):
		currentState = queue.popleft()
		#print("current state")
		#print(currentState)
		#print('queue')
		newStatesMarked.append(currentState)
		nextStates = list()
		for a in alphabets:
			#print(len(alphabets))
			nextStates = list()
			if currentState:
				#print("current state is")
				#print(currentState)
				for eachState in currentState:
					v = tuple((int(eachState), a))
					#print(transition_NFA)
					if v in transition_NFA:
						#print("v is " + str(v))
						for x in transition_NFA[v]:
							if x not in nextStates:
								nextStates.append(x)
								#print('x is' + str(x))
				# Check what state the next states could be in 
				# with the episilon transitions
				#print(nextStates)
				#print(currentState)


				epsilonTransition(nextStates, currentState)
				# Add to the new transition function
				nextStates = sorted(nextStates)
			else:
				nextStates = currentState	
				#print(nextStates)

			DFATransitions[tuple((tuple(currentState,), a))] = nextStates

			if ((sorted(nextStates) not in queue) 
				and (sorted(nextStates) not in newStatesMarked)):
				queue.append(sorted(nextStates))
	#Covert from set of one states to set of integers
	print("Printing DFA transiton")
	print(DFATransitions)
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
				#print(curState)	
				v = tuple((int(eachState), "e"))
				if v in transition_NFA:
					mult = transition_NFA[v]
					for x in mult:
						#print('printing x')
						#print(x)
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
	print(startState)

	nextStates = list()
	nextStates.extend(startState)
	while (checkForE):
		curState = checkForE.popleft()
		#print("current state")
		#print(curState)
		for eachState in curState:
			eachState = int(eachState)
			#print("eachState")
			#print(eachState)
			if eachState not in sorted(checkedForE):
				checkedForE.append(eachState)
				# search for any epsilon transitions
				v = tuple((int(eachState), "e"))
				#print('v')
				#print(v)
				if v in transition_NFA:
					#print(transition_NFA[v])
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
	print(nextStates)
	startStateAfterE = sorted(nextStates)
	print("Starte staate after e")
	print(startStateAfterE)


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
	print('new transitions')
	print(DFATransitions)

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
	print("ACCEPTING STATES")
	print(acceptingStates)
	print(lookup)
	# lookup new accept states
	for keys in lookup:
		for s in acceptingStates:
			if (s in keys):
				newAcceptStates.add(lookup[keys])




"""
 Function: writeDFAtoFile
 Arguments: fileName
 Description:
	Takes in filename and write the created dfa 
	into a user specific file.
"""




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
		print(alphabets)

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

		print(inputs)



def checkDFAInput():
	currentState = newStartState
	print("start")
	print(newStartState)
	print(newDFATransition)
	print(newAcceptStates)
	print(inputs)
	if (inputs) :
		with open(resultFile, 'w') as f:

			for val in inputs:
				currentState = newStartState
				#empty strings should be accepted only
				# if the accepting state was same as the current sate
				if len(val) == 0:
					if currentState in newAcceptStates:
						print("true")
						f.write("true\n")
					else:
						print("False")
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
						print("true")
						f.write("true\n")

					else:
						print("False")
						f.write("false\n")


# Setting up the tree


# Nodes to represent tree nodes in the syntax tree
# Note: * operator only has a left child
class Node:
	def __init__(self, value, left=None, right=None):
		self.value = value
		self.left = left
		self.right = right
	def __str__(self):
		return str(self.value)

# Function to print the values in the syntax tree
def print_tree(node, level=0):
	if node == None: return
	print('\t' * level + node.value)
	print_tree(node.left, level + 1)
	print_tree(node.right, level + 1)

# Parse the regular expression to create a syntax tree
def setUpTheNodesInTree(expression):
	global root
	operatorStack = []
	operandsStack = []
	print(expression)
	

	for i in expression:
		print('operands stack')
		for a in operandsStack:
			print(a)
		print('operator stack')
		print(operatorStack)
		print('processing i')
		print(i)
		
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

					print("Invalid expression")
					f.write("Invalid expression")
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
						print(op)
						print(i)
						print('op >= i')
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
			print(i)
			with open(resultFile, 'w') as f:
				print("Invalid expression")
				f.write("Invalid expression")			
				exit()
	# There are no more characters to scan
	# Empty the operator stack and create new syntax tree for each operator
	while(len(operatorStack) > 0):
		op = operatorStack.pop()
		createNewSyntaxTree(op, operandsStack, operatorStack)
	# Pop the root of the syntax tree off the operand stack
	root = operandsStack.pop()
	print("printing syntax tree")
	print_tree(root)



# Creates a new syntax tree from operandsStack depending on operation
# and adds it back onto the operands stack
def createNewSyntaxTree(op, operandsStack, operatorStack):
	# Create syntax tree node from op

	"""	print('creating new syntax tree for')
	print(op)
	"""
	with open(resultFile, 'w') as f:
 
		if(op == '*'):
			if(len(operandsStack) == 0):
				print("Invalid expression")
				f.write("Invalid expression")
				exit()
			left = operandsStack.pop()
			x = Node(op, left)
		else:
			if(len(operandsStack) == 0):
				print("Invalid expression")
				f.write("Invalid expression")
				exit()
			right = operandsStack.pop()
			if(len(operandsStack) == 0):
				print("Invalid expression")
				f.write("Invalid expression")
				exit()
			left = operandsStack.pop()
			x = Node(op, left, right)
		# push new syntax tree onto operands stack
		operandsStack.append(x)

class NFAObject:
	states = list()
	accept = list()
	def __init__(self, start, states, accept, transition):
		self.start = start
		self.states = states
		self.accept = accept
		self.transition = transition

def helperSyntaxTreeToNFA(val):
	global startState
	global finalNFA
	global transition_NFA
	finalNFA = syntaxTreeToNFA(val)
	print("Final NFA")
	print(vars(finalNFA).items())
	startState = finalNFA.start
	print("start state is" + str(startState))
	print("FINAL NFA ACCEPT")
	print(finalNFA.accept)
	acceptingStates.update(finalNFA.accept)
	print(acceptingStates)
	numberOfStates = len(finalNFA.states)
	print(numberOfStates)
	transition_NFA = finalNFA.transition
	transition_NFA = dict((k,v) for k,v in transition_NFA.items())

	print(transition_NFA)

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
		print("syntaxTreeToNFA")
		print(left)
		print(vars(left).items)
		print(right)
		print(vars(right))
		return concat(left, right)
	elif (current == '|'):
		if val.left:
			left = syntaxTreeToNFA(val.left)
		if val.right:
			right = syntaxTreeToNFA(val.right)
		return union(left, right)



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
def emptySet():
	states = list()
	states.append(stateNumber)
	trans = defaultdict()
	accept = list()
	start = [stateNumber]
	stateNumber = stateNumber + 1
	return NFAObject(start, states, accept, trans )
	print('empty')
def union(left, right):
	print("in union")
	print(left)
	print(vars(left).items())
	print(right)
	print(vars(right).items())
	global stateNumber
	newStart = stateNumber
	newStates = right.states + left.states
	newStates.append(newStart)
	print("printing newstates in union")
	print(newStates)
	transition = defaultdict()
	r = right.start
	print(type(r))
	l = left.start
	print("printing type")
	print(r + l)
	transition[tuple((newStart, 'e'))] = right.start + left.start
	transition.update(right.transition)
	transition.update(left.transition)
	accept = right.accept + left.accept
	stateNumber = stateNumber + 1
	return NFAObject([newStart], newStates, accept, transition)

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

def concat(left, right):
	print("in concat")
	print(left)
	print(vars(left).items())
	print(right)
	print(vars(right).items())
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

processingActions = {
	'e': epsilon,
	'N': emptySet,
	'|': union,
	'*': star,
	'`':concat,
}

concatedExpressionList = []
#make the concatination shown for ace of putting it in the tree
def makeConcatToAppear(expression):
	concatExp = ''
	print(expression)
	print ('length of expression is ' + str(len(expression)))
	if (len(expression)>1):
		for i in range(len(expression)-1):
			currentChar = expression[i]
			print('currentChat ' + currentChar)
			nextChar = expression[i+1]
			print('nextChar ' + nextChar)

			#Have if statment to check for epsilon and empty expressions
			if not currentChar and not nextChar:
				#I am not sure what should happen if we scan a empty expression 
				break
			if ((currentChar == ')' or currentChar == '*' or ((currentChar not in processingActions) and currentChar != '('))
	            and (nextChar == '(' or ((nextChar not in processingActions) and nextChar != ')'))):
				concatExp += currentChar + '`'
				print('hello')
			else:
				concatExp +=currentChar
		print(concatExp)
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
		print('Printing fully concat list')
		print(concatedExpressionList)
		for regex in concatedExpressionList:
			setUpTheNodesInTree(regex)
		helperSyntaxTreeToNFA(root)
		conversionToDFA()
		checkDFAInput()
