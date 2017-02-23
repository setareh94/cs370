import sys
import os

numberOfStates = 0
alphabets = []
states = {} 
transition = {}
def readFile(s):
	f = open(s,'w')

	numberOfStates = f.readline()
	x = f.readline()
	alphabets = list(x)
	m = f.readline()
	while( "'" in m):

		a,b,c = m.split()
		b = b.split("'")




		
		m = f.readline()




def main:
	readFile(sys.argv[0])



