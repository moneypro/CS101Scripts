import glob, sys
from numpy import isclose

correctAnswers = {
	"C2": 1e-10,
	"C3": 1e-9,
	"C4": 1e-6,
	"C5": 1e-2,
	"C6": 1e+3,
	"C7": 3.0857e+16,
	"C8": 2.54e-2,
	"C9": 0.3048,
	"C10": 1609.344,
	"C12": 0.3106855961,
	"B15": 3.1415926536,
	"B16": 0
}

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

def assertContain(arr, coords, answer):
	row, col = coordsToIndex(coords)
	if isclose(float(arr[row][col]), answer):
		return 1
	else:
		return 0

def gradeContent(arr):
	'''
	Take a 2d array, and return the similarity normalized.
	'''
	total_correct = 0
	for coords, answer in correctAnswers:
		total_correct += assertContain(arr, coords, answer)
	return total_correct / len(correctAnswers)

def readFile():
	'''
	Read file from path given in sys.argv glob.
	'''
	filenames = glob.glob(sys.argv[1])
	for filename in filenames:
		with open(filename) as f:
			content = f.readlines()
			arr = [line.strip().split(',') for line in content]
			print (gradeContent(arr))

