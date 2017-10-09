'''
Command line basis.
TODO:
1) Save the partner information.
2) Add adding name / workstation number features.
'''
import sys, random
if len(sys.argv) < 3:
    print ("Usage: python inLab.py csvFromCompass.csv sectionNo")
file = open(sys.argv[1])
raw_content = file.readlines()
file.close()
header = raw_content[0].strip().split(',')
fname_col = lname_col = netid_col = sectionNo = availNo = -1
for i in range(len(header)):
    if header[i].find("First Name")>-1: #Or some other column name
        fname_col = i #Beware cases
    if header[i].find("Last Name")>-1:
        lname_col = i
    if header[i].find("Username")>-1:
        netid_col = i
    if header[i].find("Section")>-1:
        sectionNo = i
    if header[i].find("Availability")>-1:
        availNo = i
assert (fname_col != -1 and lname_col != -1 and netid_col != -1 and sectionNo != -1 and availNo != -1)
students = {}
print (netid_col,fname_col,lname_col)
for line in raw_content[1:]:
    line = line.strip().split(',')
    section = line[sectionNo].strip('"')
    avail = line[availNo].strip('"') == 'Yes'
    if section[-1] == sys.argv[-1][-1] and avail:
        netid = line[netid_col].strip('"')
        fname = line[fname_col].strip('"')
        lname = line[lname_col].strip('"')
        students[netid] = (fname,lname)
# Or size of map
# be able to delete several students & seats
assert (len(students) <= 41)
rando = [i+1 for i in range(41)]

def randomize():
    random.shuffle(rando)
    for i, key in enumerate(students):
        value = students[key]
        try:
            students[key] = (value[0],value[1],str(rando[i]))
        except:
            students[key] = (value[0],value[1])

def printInfo():
    tuples = sorted([(i,)+students[i] for i in students],key=lambda x:x[1]) # By first name
    for t in tuples:
        output = t[1] + '\t' + t[2][0] + '\t' + t[-1]
        print (output)

while True:
    print ("(size of students) netids loaded. Enter 'p'/'print' to print them all. Enter 'd netid' to delete specific netids. Enter 'r WorkstationNo.' to remove it from random generation. Enter 'g' to generate.")
    randomize()
    printInfo()
    cmd = input()
    if cmd == 'print' or cmd=='p':
        printInfo()
    elif cmd[0] =='d': # delete student id
        netid = cmd[2:]
        if netid in students:
            del students[netid] #Or something
    elif cmd[0] == 'r': # remove seat no
        wsNo = int (cmd[2:])
        rando.remove(wsNo)
    elif cmd == 'g':
        randomize()