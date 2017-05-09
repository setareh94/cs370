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

		# m = f.readline()
		m = f.readline()

		while m:
			regularExpressionList.append(m.strip("\n"))
			setUpTheNodesInTree(m.strip("\n"))
			m = f.readline()

		print(regularExpressionList)

#Setting up the tree

processingActions = {
	'e': epsilon,
	'N': emptySet,
	'|': union,
	'*': star,
}


def setUpTheNodesInTree(expression):
	operatorStack = []
	operandsStack = []
	for i in expression:
		if i == '(':
			operandsStack.append(i)
		else if i == ')':
			operandsStack.remove()
			while (i != '(' and len(operatorStack)>0):
			# we need to pass in whatever the expression is here
				operandsStack.append() #TO-DO
		else if(i in processingActions):
			while(len(operatorStack)>0):
				op = operatorStack.remove()
				#we need to check if it is not '(' and the precedence of the character




def epsilon():
	if ch == '':
		menu_actions['main_menu']()
def emptySet():

def union():

def star():

def processingTree():



if __name__ == '__main__':
	readFile(sys.argv[1])