import os
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ARGS_CATEGORY = sys.argv[1]
SOURCEPATH = "input_parts/" + ARGS_CATEGORY
TARGETPATH = "input_full/"

print "# generating..."

fp = open(TARGETPATH + os.sep + ARGS_CATEGORY + "_input.txt", "w")

FILES = os.listdir(SOURCEPATH)
for f in FILES:
	tfp = open(SOURCEPATH + os.sep + f, "r")
	while 1:
		line = tfp.readline()
		if not line:
			break
		fp.write(line)
	tfp.close()

fp.close()
print "# done."