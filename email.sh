# Example bash email.sh 00 AYX (grade lab00 for AYX)
path=/class/cs101/etc/sxns/$2/feedback/
endpath=/lab$1/*.html
emailappend=@illinois.edu
cd /class/cs101/etc/sxns/$2/
for netid in netidlists 
do
	nbgrader feedback --assignment=lab$1 --student=$netid --quiet
	if [ -f $path$netid$endpath ]; then
		echo "Please disregard the scores for free-response coding questions. \nThis is your Lab"$1". You can also access it on EWS linux systems. Please reply to your TA's email if you have questions." | mail -a $path$netid$endpath -s "<No-Reply> CS 101 Lab $1 Feedback" $netid$emailappend
	else
		echo $netid" failed sending. File doesn't exist."
	fi
done
cd -
