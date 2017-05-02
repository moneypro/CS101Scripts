# Run it under AY? 
# Example bash email.sh 00 (grade lab00)
path=./feedback/
endpath=/lab$1/lab$1.html
emailappend=@illinois.edu 
for netid in jdalexa2 tallens2 carrea2 abenna2 andrewb2 evalina2 kdbrown3 yinhuai2 jennamc2 pgc2 agd2 kmdixit2 ddonofr2 dme2 eefoley2 jgagnon2 avg2 jhabana2 clh2 jacobch2 haoweih2 msj2 tmk2 gkim82 mkorzen2 loth2 belower2 cmalon5 mateusz3 mercers2 eleanor2 vo6 kspugh2 rqu3 srashed2 armins2 sungjin2 siil2 mateusz2 vvarada2
do
	nbgrader feedback --assignment=lab$1 --student=$netid --quiet
	if [ -f $path$netid$endpath ]; then
		echo "Please disregard the scores for free-response coding questions. \nThis is your Lab"$1". You can also access it on EWS linux systems." | mail -a $path$netid$endpath -s "CS 101 Lab $1 Feedback" $netid$emailappend
	else
		echo $netid" failed sending. File doesn't exist."
	fi
done
