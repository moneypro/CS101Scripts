from nbgrader.api import Gradebook
import sys

def extract_grades(labSec, aNo):
    labSec = "AY"+labSec if len(labSec) == 1 else labSec
    gb = Gradebook('sqlite:////class/cs101/etc/sxns/'+labSec+'/gradebook.db')
    aNo = "lab" + aNo if len(aNo) == 2 else "lab0" + aNo
    grades = {}
    #print (gb.assignment_submissions)
    for s in gb.assignment_submissions(aNo):
        grades[s.student_id] = float(s.score)
    return grades

if __name__ == "__main__":
    grade = extract_grades(sys.argv[1], sys.argv[2])
    for netid, score in grade.items():
        print (netid, score)