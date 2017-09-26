# Run it under AY? 
# Example bash email.sh 00 (grade lab00)
path=/class/cs101/etc/sxns/$2/feedback/
endpath=/lab$1/*.html
emailappend=@illinois.edu
for netid in lunanli3 
do
	nbgrader feedback --assignment=lab$1 --student=$netid --quiet
	if [ -f $path$netid$endpath ]; then
		echo "Please disregard the scores for free-response coding questions. \nThis is your Lab"$1". You can also access it on EWS linux systems." | mail -a $path$netid$endpath -s "CS 101 Lab $1 Feedback" $netid$emailappend
	else
		echo $netid" failed sending. File doesn't exist."
	fi
done
