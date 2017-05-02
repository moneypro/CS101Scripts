import sys, subprocess, os
if (len(sys.argv)<3):
	print ("Usage: python collabsEmail.py collabs.txt labNo")
netidList = "jdalexa2 tallens2 carrea2 abenna2 andrewb2 evalina2 kdbrown3 yinhuai2 jennamc2 pgc2 agd2 kmdixit2 ddonofr2 dme2 eefoley2 jgagnon2 avg2 jhabana2 clh2 jacobch2 haoweih2 msj2 tmk2 gkim82 mkorzen2 loth2 belower2 cmalon5 mateusz3 mercers2 eleanor2 vo6 kspugh2 rqu3 srashed2 armins2 sungjin2 siil2 mateusz2 vvarada2".split()
labNo = sys.argv[2]
subject = "Lab"+labNo+" Feedback"
content = "This is a resent for lab07, given that a lot of you did not get proper appendix last time."
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
		filePath = "./feedback/"+submitter+"/lab"+labNo+"/lab"+labNo+".html"
		subprocess.call(['nbgrader', 'feedback', '--assignment=lab'+labNo, '--student='+submitter, '--quiet'])
		if os.path.isfile(filePath):
			subprocess.call("mail -s '"+subject+"' "+toAddr+" <<<'"+content+"'", shell=True)
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
				subprocess.call("mail -s '"+subject+"' "+toAddr+" <<<'"+content+"'", shell=True)
				sentTrack[collab] = True
				print (collab+" shared "+ submitter+" sent.")
for netid in sentTrack:
	if sentTrack[netid] == False:
		print (netid+" not sent.")

				
