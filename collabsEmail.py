import sys, subprocess, os, glob
from ultimateGradeCal import getCollabs
from extract_info import extract_info
if (len(sys.argv) < 4):
	print ("Usage: python collabsEmail.py csv labSec labNo")
	exit (1)
csvFileName = sys.argv[1]
labSec = sys.argv[2] if len(sys.argv[2]) == 3 else "AY" + sys.argv[2]
labNo = sys.argv[3] if len(sys.argv[3]) == 2 else "0" + sys.argv[3]
netidList = list(extract_info(csvFileName, labSec))
subject = "No-Reply: Lab"+labNo+" Feedback"
content = "This is a test send for lab"+labNo+". Please reply to my email address hcheng17@illinois.edu if you have questions."
sentTrack={}
collabSendingList = []
for netid in netidList:
	sentTrack[netid]= False
collabs = getCollabs(labSec[-1], labNo)
path = "/class/cs101/etc/sxns/"+labSec

# Generate feedbacks
os.chdir(path)
for submitter in collabs:
	filePath = glob.glob(path + "/feedback/"+submitter+"/lab"+labNo+"/*.html")
	if len(filePath) == 0:
		subprocess.call(['nbgrader', 'feedback', '--assignment=lab'+labNo, '--student='+submitter, '--quiet'])

# Send to the submitters
for submitter in collabs:
	# Call subprocess
	toAddr = submitter+"@illinois.edu"
	filePath = glob.glob(path + "/feedback/"+submitter+"/lab"+labNo+"/*.html")
	if len(filePath) != 0:
		filePath = filePath[0]
		subprocess.call("mail -s '"+subject+"' -a "+filePath+' '+toAddr+" <<<'"+content+"'", shell=True)
		sentTrack[submitter] = True
		collabSendingList.append(submitter)
		print (submitter+" sent.")
	else:
		print("Submitter file doesn't exist. It shouldn't be possible though...")

# Send to the collaborators
for submitter in collabSendingList:
	for collab in collabs[submitter]:
		if collab in netidList and collab!=submitter:
			#send email
			filePath = glob.glob(path + "/feedback/"+submitter+"/lab"+labNo+"/*.html")
			toAddr = collab+"@illinois.edu"
			subprocess.call("mail -s '"+subject+"' -a "+filePath[0]+' '+toAddr+" <<<'"+content+"'", shell=True)
			sentTrack[collab] = True
			print (collab+" shared "+ submitter+" sent.")

# Tract unsent net ids
for netid in sentTrack:
	if sentTrack[netid] == False:
		print (netid+" not sent.")

				
