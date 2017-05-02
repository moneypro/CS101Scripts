import glob
def getCollabs(labNo):
    collabs = {} # to return
    files = glob.glob("submitted/*/lab"+labNo+"/lab"+labNo+".ipynb")
    from string import whitespace as w
    from string import punctuation as p
    from string import printable
    featureTxt = "Double-click here to list collaborators' or partners' **NetIDs** here:"
    for f in files:
        with open(f) as openF:
            data = openF.read()
            cell=data[data.find(featureTxt):data.find('lab'+labNo)]
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
            submitter = f.split("/")[1]
            collabsList = sanitized.split(' ')
            for i in range(len(collabsList)):
                collabsList[i] = collabsList[i].strip()
            collabs[submitter] = collabsList
    return collabs

print(getCollabs("07"))