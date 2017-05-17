import os
import filecmp

for i in range(1,20):
	v = "python p03.py" +" testcasesUnix/re" +str(i)+"In.txt" +" input.txt"
	print(v)
	os.system(v)
	file = "testcasesUnix/re" + str(i)+"Out.txt"
	print(filecmp.cmp(file, 'input.txt'))