from operator import itemgetter
import cPickle
import jieba
import jieba.posseg as pseg
jieba.load_userdict("/home/chris/MyCrawel/dicts/0.txt")
jieba.load_userdict("/home/chris/MyCrawel/dicts/1.txt")
jieba.load_userdict("/home/chris/MyCrawel/dicts/2.txt")
jieba.load_userdict("/home/chris/MyCrawel/dicts/3.txt")
jieba.load_userdict("/home/chris/MyCrawel/dicts/4.txt")
import re
import os
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ARGS_CATEGORY = sys.argv[1]
ARGS_SOURCEPATH = "data/" + ARGS_CATEGORY
ARGS_TARGETPATH = "freqs/" + ARGS_CATEGORY 

FILES = os.listdir(ARGS_SOURCEPATH)
for f in FILES:
	FULLPATH = ARGS_SOURCEPATH + os.sep + f
	fp = open(FULLPATH,"r")
	contents = ""
	print "# Reading %s" %f
	while 1:
		line = fp.readline()
		if not line:
			break
		contents += line
	fp.close()
	MyDict = {}
	print "# Cutting %s" %f
	res = pseg.cut(contents)
	print "# Calculating %s" %f
	for w in res:
		if not MyDict.has_key(w.word):
			MyDict[w.word] = 1
		else:
			MyDict[w.word] += 1

	# sort
	# sDict = sorted(MyDict.items(), key=itemgetter(1), reverse=True)

	# serialize, for middleware
	# create a file if not exist
	fp = open(ARGS_TARGETPATH + os.sep + f[0:-4] + ".seq","w")
	fp.close()
	print "# Serializing %s" %f
	cPickle.dump(MyDict,open(ARGS_TARGETPATH + os.sep + f[0:-4] + ".seq","wb"))

	print "# done."
	# for k in sDict:
	# 	print "%s,%s" %(k[0],k[1])
