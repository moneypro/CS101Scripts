from hw01heat import hw01heat
from hw01matrix import hw01matrix
from hw01gears import hw01gears
import sys

def getHw1Score():
    scores = [hw01gears, hw01heat, hw01matrix]
    grade = {}
    errors = set()
    for d in scores:
        for key, value in d.items():
            value = value *2 /3
            if value <= 0:
                errors.add(key)
                value = 0
            if key in grade:
                grade[key] += value
            else:
                grade[key] = value
        # print (errors)
    return grade

if __name__ == '__main__':
    grade = getHw1Score()
    if len(sys.argv) < 2:
        print(grade)
    else:
        print ([(key, hw01gears[key], hw01heat[key], hw01matrix[key]) for key in grade if key in sys.argv[1:]])