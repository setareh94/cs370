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
newStatesMarked = list()
stringsList = []
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

		x = f.readline()
		alphabets = list((x.strip("\n")))
		print(alphabets)

		# Read in the Regular Expression
		m = f.readline()
		m = m.strip(" ")
		m = m.strip("\n")
		makeConcatToAppear(m)

		# Create syntax tree

		# setUpTheNodesInTree(m.strip("\n"))
		m = f.readline()

		# Read in the inputs
		while m:
			# setUpTheNodesInTree(m.strip("\n"))

			stringsList.append(m.strip("\n"))
			m = f.readline()

		print(stringsList)

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
def print_tree(node):
	if node == None: return
	print(node.value)
	print_tree(node.left)
	print_tree(node.right)

# Parse the regular expression to create a syntax tree
def setUpTheNodesInTree(expression):
	operatorStack = []
	operandsStack = []
	print(expression)
	
	# TODO: add implied concats


	# TODO: add epsilons

	for i in expression:
		"""		print('operands stack')
		for a in operandsStack:
			print(a)
		print('operator stack')
		print(operatorStack)
		print('processing i')
		print(i)
		"""
		# Check if symbol from the alphabet
		if(i in alphabets):
			x = Node(i)
			operandsStack.append(x)
		elif i == '(':
			operatorStack.append(i)
		elif(i == ')'):
			# pop operators off stack until ( is popped off
			v = operandsStack.pop()
			while (v != '(' and len(operatorStack) > 0):
				# create new syntax tree and add it to operands stack
				createNewSyntaxTree(v, operandsStack, operatorStack)
				v = operandsStack.pop()
		# Check if an operator
		elif(i in processingActions):
			if(len(operatorStack) > 0):
				op = operatorStack.pop()
				# check if op has a greater than or equal precedence to operator just scanned
				# precedence is star highest, then concatenation, then union
				if((op == '*') | (op == '.' and i != '*') | (op == '|' and i == '|')):
					# op >= i
					# create new syntax tree and add it to operands stack
					createNewSyntaxTree(op, operandsStack, operatorStack)
					# push operand just scanned onto stack
					operatorStack.append(i)
				else:
					# op < i
					# push op back onto the operator stack and i
					operatorStack.append(op)
					operatorStack.append(i)
			else:
				# operator stack is empty
				operatorStack.append(i)
		else:
				#invalid expression throw error
			print(i)
			print('Invalid expression')
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
	if(op == '*'):
		if(len(operandsStack) == 0):
			print("ERROR with expression")
		left = operandsStack.pop()
		x = Node(op, left)
	else:
		if(len(operandsStack) == 0):
			print("ERROR with expression")
		right = operandsStack.pop()
		if(len(operandsStack) == 0):
			print("ERROR with expression")
		left = operandsStack.pop()
		x = Node(op, left, right)
	# push new syntax tree onto operands stack
	operandsStack.append(x)



def epsilon():
	if ch == '':
		menu_actions['main_menu']()
def emptySet():
	print('empty')
def union():
	print("union")
def star():
	print('star')
def processingTree():
	print("processingTree")
def concat():
	print('concat')

processingActions = {
	'e': epsilon,
	'N': emptySet,
	'|': union,
	'*': star,
	'.':concat,
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
				concatExp += currentChar + '.'
				print('hello')
			else:
				concatExp +=currentChar
		print(concatExp)
		fullyConcat =  concatExp + expression[len(expression)-1]
		concatedExpressionList.append(fullyConcat)
	else:
		concatedExpressionList.append(expression)




if __name__ == '__main__':
	readFile(sys.argv[1])
	print('Printing fully concat list')
	print(concatedExpressionList)
	for regex in concatedExpressionList:
		setUpTheNodesInTree(regex)
