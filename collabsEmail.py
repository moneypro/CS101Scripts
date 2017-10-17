import sys, subprocess, os
if (len(sys.argv) < 4):
	print ("Usage: python collabsEmail.py collabs.txt labSec labNo")
netidList = "jdalexa2 tallens2 carrea2 abenna2 andrewb2 evalina2 kdbrown3 yinhuai2 jennamc2 pgc2 agd2 kmdixit2 ddonofr2 dme2 eefoley2 jgagnon2 avg2 jhabana2 clh2 jacobch2 haoweih2 msj2 tmk2 gkim82 mkorzen2 loth2 belower2 cmalon5 mateusz3 mercers2 eleanor2 vo6 kspugh2 rqu3 srashed2 armins2 sungjin2 siil2 mateusz2 vvarada2".split()
labSec = sys.argv[2] if len(labSec) == 3 else "AY" + labSec
labNo = sys.argv[3] if len(labNo) == 2 else "0" + labNo
subject = "No-Reply: Lab"+labNo+" Feedback"
content = "This is a test send for lab05. Please reply to my email address hcheng17@illinois.edu if you have questions."
sentTrack={}
collabSendingList = []
for netid in netidList:
	sentTrack[netid]= False
with open(sys.argv[1]) as f:
	data = f.readlines()
	collabs = {}
	for line in data:
		line = line.strip()
		if line == "":
			continue
		line = line.split(" ")
		if len(line)<=1:
			continue
		collabs[line[0]]= line[1:]
	for submitter in collabs:
		# Call subprocess
		toAddr = submitter+"@illinois.edu"
		filePath = "/class/cs101/etc/sxns/"+labSec+"/feedback/"+submitter+"/lab"+labNo+"/lab"+labNo+".html"
		subprocess.call(['nbgrader', 'feedback', '--assignment=lab'+labNo, '--student='+submitter, '--quiet'])
		if os.path.isfile(filePath):
			subprocess.call("mail -s '"+subject+"' -a "+filePath+toAddr+" <<<'"+content+"'", shell=True)
			sentTrack[submitter] = True
			collabSendingList.append(submitter)
			print (submitter+" sent.")
		else:
			print("Submitter file doesn't exist. It shouldn't be possible though...")
	for submitter in collabSendingList:
		for collab in collabs[submitter]:
			if collab in netidList and collab!=submitter:
				#send email
				toAddr = collab+"@illinois.edu"
				subprocess.call("mail -s '"+subject+"' -a "+filePath+toAddr+" <<<'"+content+"'", shell=True)
				sentTrack[collab] = True
				print (collab+" shared "+ submitter+" sent.")
for netid in sentTrack:
	if sentTrack[netid] == False:
		print (netid+" not sent.")

				
