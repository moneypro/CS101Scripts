import glob, sys
if len(sys.argv)!=2 or len(sys.argv[1])!=2:
	print ("Usage: python collabs LabNo(i.e. 01)")
	exit(1)
labNo = sys.argv[1]
files = glob.glob("submitted/*/lab"+labNo+"/lab"+labNo+".ipynb")
from string import whitespace as w
from string import punctuation as p
from string import printable
featureTxt = "Double-click here to list collaborators' or partners' **NetIDs** here:"
for f in files:
	#print(f)
	with open(f) as openF:
		data = openF.read()
		cell=data[data.find(featureTxt):data.find('lab'+labNo)]
		#print('New_file')		
		#print(cell)
		names=cell[len(featureTxt):cell.find(']')][:-1]
		label='write them here'
		if label in names:
			names=names[names.find(label)+ len(label) :]
		#print('names now')		
		#print(names)
		for c in w + p:
			names = names.replace(c, " ")		
		names = names.split(' ')
		names = [x for x in names if x != '']
		collabsList = ' '.join(names)
		sanitized=""
		for letter in collabsList:
			if letter in printable:
				sanitized+=letter
		print (f.split("/")[1],sanitized)




		# cell=data[data.find('beyond the TA or the help files'):data.find('This laboratory exercise was written by Neal Davis')]
		# names=cell[135:-80]
		# label='Double-click here to add collaborators or partners'
		# if label in names:
		# 	names=names[names.find(label)+ len(label) :]
		# #print(names)
		# for c in w + p:
		# 	names = names.replace(c, " ")		
		# names = names.split(' ')
		# names = [x for x in names if x != '']
		# print(f.split("/")[1], ' '.join(names))
