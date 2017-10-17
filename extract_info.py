import sys

def extract_info(csvfilename, labSec, availOnly = True):
    with open(csvfilename,'r') as f:
        fileContent = f.readlines()
        headers = fileContent[0].strip().split(',')
        netidNo = -1
        sectionNo = -1
        availNo = -1
        fileOutput = {} # dict of lists
        for i in range(len(headers)):
            if headers[i].find("Username")>-1:
                netidNo = i
            if headers[i].find("Section")>-1:
                sectionNo = i
            if headers[i].find("Availability")>-1:
                availNo = i
        if netidNo == -1 or sectionNo == -1 or availNo == -1:
            raise ValueError("CSV file doesn't have all necessary columns.")          
        for line in fileContent[1:]:
            line = line.strip().split(',')
            netid = line[netidNo].strip('"')
            section = line[sectionNo].strip()[-2]
            avail = line[availNo].strip('"') == 'Yes'
            if section == labSec[-1] and (avail or not availOnly):
                fileOutput[netid] = line.copy()
    return fileOutput

if __name__ == "__main__":
    if len(sys.argv)<3:
        print ("Usage: python extract_info.py compassScores.csv labSec({A,B,..,Q})")
        exit(1)
    csvfilename = sys.argv[1]
    labSec = sys.argv[2]
    print (extract_info(csvfilename, labSec))