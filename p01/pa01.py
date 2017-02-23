import sys
import os
from collections import defaultdict

numberOfStates = 0
alphabets = []
states = {} 
transition = defaultdict(set)
startState
acceptingStates = []
inputs = []
def readFile(s):
	f = open(s,'w')

	numberOfStates = f.readline()
	x = f.readline()
	alphabets = list(x)
	m = f.readline()
	while( "'" in m):
		a,b,c = m.split()
		b = b.split("'")
		transition[(a, b)] = c
		m = f.readline()
	startState = m
	acceptingStates = f.readline().split()
	l = f.readline()
	while l
		inputs.add(m)
		l = f.readline()



def main:
	readFile(sys.argv[0])



