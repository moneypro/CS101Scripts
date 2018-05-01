import sys, glob
def getCollabs(labSec, labNo):
    collabs = {} # to return
    files = glob.glob("/class/cs101/etc/sxns/AY"+labSec+"/submitted/*/lab"+labNo+"/*.ipynb")
    from string import whitespace as w
    from string import punctuation as p
    from string import printable
    featureTxt = '"collaborators = ['
    for f in files:
        with open(f) as openF:
            data = openF.read()
            cell=data[data.find(featureTxt):]
            names=cell[len(featureTxt):cell.find(']')][:-1]
            label='write them here'
            if label in names:
                names=names[names.find(label)+ len(label) :]
            for c in w + p:
                names = names.replace(c, " ")       
            names = names.split(' ')
            names = [x for x in names if x != '']
            collabsList = ' '.join(names)
            sanitized=""
            for letter in collabsList:
                if letter in printable:
                    sanitized+=letter
            path = f.split("/")
            submitter = path[path.index('submitted')+1]
            # print (submitter)
            collabsList = sanitized.split(' ')
            for i in range(len(collabsList)):
                collabsList[i] = collabsList[i].strip()
            collabs[submitter] = collabsList
    # print (collabs)
    return collabs

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Extract collaborators from NB grader and output collab info')
    parser.add_argument('section', metavar='{A-Q}', nargs='?', help='section name (one character)')
    parser.add_argument('no' , metavar='XX', nargs='?', help='labNo')
    
    args = parser.parse_args()
    print (getCollabs(args.section, args.no))