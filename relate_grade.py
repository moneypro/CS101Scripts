import sys
from numpy import isclose
from lab01.lab01 import correctAnswers

def getIdFromPath(path):
	'''
	/home/hcheng17/cs101-fa17/lab00subs/zz23@illinois.edu.txt
	-> zz23
	'''
	return path[path.rfind('/')+1:path.rfind('@')]


def coordsToIndex(excelCoords):
	'''
	Convert ONE pair of Excel coordinates to Python 2d array coords.
	C2 -> (2, 1)
	TODO: Use regular expressions
	'''
	from string import ascii_letters, digits
	rowCoord = ""
	colCoord = ""
	for s in excelCoords:
		if s in ascii_letters:
			rowCoord += s 
		if s in digits:
			colCoord += s
	row = ord(rowCoord) - ord('A') # Only works if length = 1
	col = int(colCoord) - 1
	return (row, col)

def assertSame(actual, answer):
	try: 
		if isclose(float(actual), answer, rtol=0.025):
			return 1
		else:
			# print (actual, answer)
			return 0
	except ValueError:
		return 0

def compareTwoArr(actual, answer):
	from hw01 import hw01
	total_correct = 0
	rowRange = range(1,len(answer))
	colRange = range(len(answer[0]))
	for row in rowRange:
		for col in colRange:
			try:
				if(hw01.assertSameHw01(answer[row][col], actual[row][col])):
					total_correct+=1
				# else:
					# print ((answer[row][col], actual[row][col]))
			except IndexError:
				break
	return total_correct / (len(rowRange)) / len(colRange)

def gradeContent(arr):
	'''
	Take a 2d array, and return the similarity normalized.
	'''
	total_correct = 0
	for coords, answer in correctAnswers.items():
		row, col = coordsToIndex(coords)
		try:
			actual = arr[col][row]
			if assertSame(actual, answer) == 1:
				total_correct += 1
			else:
				if 'errors' in globals():
					errors[coords] +=1
		except IndexError:
			# print ('IndexError')
			continue
	return total_correct / len(correctAnswers) + 1 # Only for lab 01

def readFileAndGrade(filenames):
	'''
	Read file from path given in filenames.
	return a dictionary of grades (id, score(normalized))
	'''
	grades = {}
	for filename in filenames:
		with open(filename) as f:
			try:
				content = f.readlines()
			except UnicodeDecodeError:
				grades[getIdFromPath(filename)] = -1 # Syntax error.
			arr = [line.strip().split(',') for line in content]
			grades[getIdFromPath(filename)] = gradeContent(arr)
	return grades

def readFileByOneReference(answerFileName, filenames):
	'''
	Compare answers in csv in answerFileName. 
	Score is standarized to 1.
	'''
	ans = []
	grades = {}
	with open(answerFileName) as f:
		content = f.readlines()
		ans = [line.strip().split(',') for line in content]
	for filename in filenames:
		with open(filename) as f:
			try:
				content = f.readlines()
				arr = [line.strip().split(',') for line in content]
				grades[getIdFromPath(filename)] = compareTwoArr(arr, ans)
			except UnicodeDecodeError:
				grades[getIdFromPath(filename)] = 0 # Syntax error.
	return grades

if __name__ == "__main__":
	# print (readFileByOneReference(sys.argv[1], sys.argv[2:]))
	errors = {}
	for key in correctAnswers:
		errors[key] = 0

	print (readFileAndGrade(sys.argv[1:]))
	print (errors)