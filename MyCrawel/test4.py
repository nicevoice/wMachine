from subprocess import *
p=Popen(['python','-u','CalcFreq.py','caijing'],shell=False,stdout=PIPE)
data=p.stdout.readline()
while 1:
	print data
	data=p.stdout.readline()
	if data.find('Calculating') != -1:
		print data
		break
print "########"
p.kill()