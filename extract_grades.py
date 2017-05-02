from nbgrader.api import Gradebook
import sys
labSec = sys.argv[1]
labSec = "AY"+labSec
gb = Gradebook('sqlite:////class/cs101/grading/'+labSec+'/gradebook.db')
ourIds = []
aNo = sys.argv[2]
aNo = "lab" + aNo
#print (gb.assignment_submissions)
for s in gb.assignment_submissions(aNo):
        if s.student_id not in ourIds:
                print(s.student_id, s.score)#, s.timestamp.isoformat())
