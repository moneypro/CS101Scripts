### Lab 01 Grading ###
Just run python ultimateGradeCal.py <Section> 01 > output.csv

Do it for each section, and upload two csv files to compass.

### UltimteGradeCal.py ###
It is one we only need if everything works out. Put it in EWS Linux environment and run it with "python ultimateGradeCal.py compass2g.csv labSec({A,B,...R} labNo({00,01,...12}) [collabs:Y/N]". It will print out the a csv file, so it is better to pipe it to a file.
The compass2g.csv file is the file downloaded from compass2G. It contains the netid, full name and lab grades. The only part matters is the netid, and the header column for the labNo. (lab{00,...,14}).
The output csv file should be uploaded back to compass2G using the same interface when downloading. To match the output file with compass, the csv file needs to have a unique id in the header column, which can be retrieved in compass.

### email.sh ###
The bash file serves generating the feedback nbgrader file and send those to the students. It is an automatic and naive solution, but notice that the "mail" command sends the email from netid@linux.illinois.edu, so you won't be able to see it in your outbox, and if students reply directly to it, you need to access it on ews machines using "mail"... There could be a way of setting up mailbox, but I haven't looked into it.

### collabsEmail.py ###
This script extracts the collabs and send the email. This uses a python shell, but still "mail" command for emailing. So it has the same problem as above.

### extract_grades.py ###
It extracts the grades with "python extract_grades.py {A,B,...R} {00,01,...12}". The only part worth noting is that the lab number is always two digits due to Neal's preference. It is a faster way to check individual's grades when we don't need to update the csv files.

### Some useful grading commmand ###
To generate Feedback for each lab:
nbgrader feedback --assignment=labXX --student==netid

Email
sh email.sh LabNo AY?

Grade a single student’s lab:
nbgrader autograde --student=netid labXX

### CS101 file directory ###
nbgrader should be run under /class/cs101/etc/sxns/AY?

/class/cs101/etc/sxns/AY?/submitted --student submission

/class/cs101/etc/sxns/AY?/atuograded --graded jupyter-notebook. Need to remove the record here if you want to grade again

/class/cs101/etc/sxns/AY?/feedback --feedback that will be sent to students