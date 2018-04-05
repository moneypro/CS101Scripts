def randomize(students):
    rando = [i+1 for i in range(len(students) + 1)]
    rando.remove(22) # Remove instructor's seat
    random.shuffle(rando)
    for i, key in enumerate(students):
        value = students[key]
        try:
            students[key] = (value[0],value[1],str(rando[i]))
        except:
            students[key] = (value[0],value[1])
    return students

def extractInfo(students):
    output = []
    tuples = sorted([(i,)+students[i] for i in students],key=lambda x:x[1]) # By first name
    for t in tuples:
        output.append (t[1] + '\t' + t[2][0] + '\t' + t[-1])
    return output

def printInfo(students):
    for o in extractInfo(students):
        print (o)

def sendEmail(students):
    if len(students) == 0 or len(students[list(students.keys())[0]]) <= 2:
        print ("Error, not generated.")
        exit(1)
    subject = "No-Reply: This weeks lab seat assignment"
    for netid, info in students.items():
        toAddr = netid + "@illinois.edu"
        content = "Your seat for the lab is "+info[-1] +"."
        subprocess.call("mail -s '"+subject+"' "+toAddr+" <<<'"+content+"'", shell=True)

def saveSeats(students, outputFileName):
    with open(outputFileName, 'w') as f:
        for o in extractInfo(students):
            f.write(o)

'''
Command line basis.
TODO:
1) Save the partner information.
2) Add adding name / workstation number features.
'''
import sys, random, subprocess, argparse

def main():

    parser = argparse.ArgumentParser(description='Print out information for lab seat assignments. Seat 22 is automatically removed.')
    parser.add_argument('csv', metavar='gc...csv', nargs='?', help='csv downloaded from Compass (comma separated)')
    parser.add_argument('section', metavar='{A-Q}', nargs='?', help='section name')
    parser.add_argument('-p', '--print', action = 'store_const', const = True, help = "Print seat assignments.")
    parser.add_argument('-e', '--email', action = 'store_const', const = True, help = "Email students immediately")
    parser.add_argument('-nl', '--noloop', action = 'store_const', const = True, help = "No loop runned.")
    parser.add_argument('-s', '--save', default = 'inLabOutput.csv', help = "Save first randomized assignment to a file.")

    args = parser.parse_args()
    csvfilename = args.csv
    labSec = args.section

    file = open(csvfilename)
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

    for line in raw_content[1:]:
        line = line.strip().split(',')
        section = line[sectionNo].strip('"')
        avail = line[availNo].strip('"') == 'Yes'
        if section[-1] == labSec[-1] and avail:
            netid = line[netid_col].strip('"')
            fname = line[fname_col].strip('"')
            lname = line[lname_col].strip('"')
            students[netid] = (fname,lname)
    # Or size of map
    # be able to delete several students & seats
    assert (len(students) <= 41)
    print (len(students))
    rando = [i+1 for i in range(41)]
    rando.remove(22) # Remove instructor's seat


    students = randomize(students)

    if args.print:
        printInfo(students)

    if args.email:
        sendEmail(students)

    saveSeats(students, args.save)

    if not args.noloop:
        while True:
            print ("""(size of students) netids loaded. 
                Enter 'p'/'print' to print them all. 
                Enter 'd netid' to delete specific netids. 
                Enter 'r WorkstationNo.' to remove it from random generation. 
                Enter 'g' to generate.
                Enter 's' to send emails of seat assignment.""")
            cmd = input()
            if cmd == 'print' or cmd=='p':
                printInfo(students)
            elif cmd[0] =='d': # delete student id
                netid = cmd[2:]
                if netid in students:
                    del students[netid] #Or something
            elif cmd[0] == 'r': # remove seat no
                wsNo = int (cmd[2:])
                rando.remove(wsNo)
            elif cmd == 'g':
                students = randomize(students)
            elif cmd == 's':
                sendEmail(students)
    # elif cmd.lower() == 'send random':
    #     sendRandomNumber()


if __name__ == '__main__':
    main()
# def sendRandomNumber():
#     import numpy as np
#     import numpy.random as npr
#     prob1 = np.array( range( 7575,7642 ) )
#     prob2 = np.array( range( 5050,5098 ) )
#     vals = np.zeros( (len(students),4),dtype=np.int16 )
#     for i in range( vals.shape[0] ):
#         vals[ i,0:2 ] = ( npr.choice( prob1, size=(2,), replace=False ) )
#         vals[ i,2: ]  = ( npr.choice( prob2, size=(2,), replace=False ) )
#     if len(students) == 0 or len(students[list(students.keys())[0]]) <= 2:
#         print ("Error, not generated.")
#     subject = "No-Reply: Four SECRET numbers for this week lab"
#     _id = 0
#     for netid, info in students.items():
#         toAddr = netid + "@illinois.edu"
#         content = "Your secret numbers are "+str(vals[_id])
#         subprocess.call("mail -s '"+subject+"' "+toAddr+" <<<'"+content+"'", shell=True)
#         _id +=1
