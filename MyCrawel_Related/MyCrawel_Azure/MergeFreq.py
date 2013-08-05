import cPickle
import os
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ARGS_CATEGORY = sys.argv[1]
ARGS_SOURCEPATH = "freqs/" + ARGS_CATEGORY
ARGS_TARGETPATH = "freqs/"

FILES = os.listdir(ARGS_SOURCEPATH)
MergedDict = {}
for f in FILES:
	FULLPATH = ARGS_SOURCEPATH + os.sep + f
	# un-serialize
	print "# unserializing %s" %f
	MyDict = cPickle.load(open(FULLPATH,"rb"))
	# iter & Merge
	print "# merging %s" %f
	for k in MyDict:
		if not MergedDict.has_key(k):
			MergedDict[k] = 1
		else:
			MergedDict[k] += MyDict[k]

# done - write back to root
print "# merge done, serializing..."
FULLTARGET = ARGS_TARGETPATH + os.sep + ARGS_CATEGORY + ".seq"
#if no exist - create it
fp = open(FULLTARGET,"wb")
fp.close()
cPickle.dump(MergedDict, open(FULLTARGET,"wb"))