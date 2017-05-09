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
regularExpressionList = []
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
		# Create syntax tree
		setUpTheNodesInTree(m.strip("\n"))
		m = f.readline()

		# Read in the inputs
		while m:
			regularExpressionList.append(m.strip("\n"))
			m = f.readline()

		print(regularExpressionList)

#Setting up the tree

processingActions = {
	'e': 'epsilon',
	'N': 'emptySet',
	'|': 'union',
	'*': 'star',
}
class Node:
	def __init__(self, value, left=None, right=None):
		self.value = value
		self.left = left
		self.right = right
	def __str__(self):
		return str(self.value)


def setUpTheNodesInTree(expression):
	operatorStack = []
	operandsStack = []
	print(expression)
	for i in expression:
		# Check if symbol from the alphabet
		if(i in alphabets):
			x = Node(i)
			operandsStack.append(x)
		elif i == '(':
			operatorStack.append(i)
		elif(i == ')'):
			# pop operators off stack until ( is popped off
			v = operandsStack.remove()
			while (v != '(' and len(operatorStack) > 0):
				# create new syntax tree and add it to operands stack
				createNewSyntaxTree(v, operandsStack, operatorStack)
				v = operandsStack.remove()
		# Check if an operator
		elif(i in processingActions):
			if(len(operatorStack) > 0):
				op = operatorStack.remove()
				# check if op has a greater than or equal precedence to operator just scanned
				# precedence is star highest, then concatenation, then union
				if((op == '*') | (op == 'concat' && i != '*') | (op == '|' && i == '|')):
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
	# There are no more characters to scan
	# Empty the operator stack
	while(len(operatorStack) > 0):



# Creates a new syntax tree from operandsStack depending on operation
# and adds it back onto the operands stack
def createNewSyntaxTree(op, operandsStack, operatorStack):
	# Create syntax tree node from op
	if(op == '*'):
		left = operandsStack.remove()
		x = Node(op, left)
	else:
		right = operandsStack.remove()
		left = operandsStack.remove()
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


if __name__ == '__main__':
	readFile(sys.argv[1])