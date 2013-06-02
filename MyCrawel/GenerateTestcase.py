import cPickle
import os
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from operator import itemgetter

# will automatically find _filtered.seq
ARGS_CATEGORY = sys.argv[1]
# input the _filtered.seq
ARGS_FILTERED = sys.argv[2]
# mark all the set the category, temporary support one number
# in this case, all set 0
# ARGS_LABEL = sys.argv[3]
ARGS_LABEL = "0"


FILEPATH = "freqs/" + ARGS_CATEGORY
SOURCEPATH = "freqs/" + ARGS_FILTERED + "_filtered.seq"
# testcases all set zero - 0
TARGETPATH = "testcases/" + ARGS_CATEGORY + "_on_" + ARGS_FILTERED + "_predict_0.txt"
# store for future merge with different labels - not used in this file
# STOREPATH = "freqs/" + ARGS_CATEGORY + "_mergedinput.seq"

fp = open(TARGETPATH,"w")

# read dimemsion definition
print "# loading %s" %SOURCEPATH
mDict = cPickle.load(open(SOURCEPATH,"rb"))

FILES = os.listdir(FILEPATH)
for f in FILES:
	print "# generating dimemsions of %s" %f
	FULLPATH = FILEPATH + os.sep + f
	cc = cPickle.load(open(FULLPATH,"rb"))
	# prepare to write into a file
	# each file input a line
	# LB = str(ARGS_LABEL)
	# if ARGS_LABEL >=0:
	# 	LB = "+" + str(ARGS_LABEL)
	# else:
	# 	LB = "-" + str(ARGS_LABEL)
	fp.write(ARGS_LABEL)
	# go every dimemsion in mDict to check, formatting tuple	
	mcount = 1
	for k in mDict:
		if not cc.has_key(k[0]):
			# tempDict[k[0]] = 0
			fp.write(" " + str(mcount) + ":0")
		else:
			# tempDict[k[0]] = k[1]
			fp.write(" " + str(mcount) + ":" + str(cc[k[0]]))
		mcount += 1
	fp.write("\n")
	

fp.close()
FINALNAME = ARGS_CATEGORY + "_on_" + ARGS_FILTERED + "_predict_0.txt"
print "# Successed. Your testcase name is: %s" %FINALNAME
print "# done."