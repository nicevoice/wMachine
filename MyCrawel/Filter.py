import cPickle
import os
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from operator import itemgetter

ARGS_CATEGORY = sys.argv[1]
# ARGS_FULLPATH = sys.argv[1]
# dimemsions trimed
ARGS_DIMENUME = string.atoi(sys.argv[2])

print "# ARGS_CATEGORY = " + ARGS_CATEGORY
print "# ARGS_DIMENUME = " + ARGS_DIMENUME

FULLPATH = "freqs/" + ARGS_CATEGORY + ".seq"
TARGETPATH = "freqs/" + ARGS_CATEGORY +  "_filtered.seq"

MergedDict = cPickle.load(open(FULLPATH,"rb"))

# eliminate those len=1
eDict = {}
for k in MergedDict:
	# eliminate \t, \n, \ ,etc.
	sk = k.strip()
	if len(sk) > 1:
		eDict[sk] = MergedDict[k]

# sort
sDict = sorted(eDict.items(), key=itemgetter(1), reverse=True)

# trim as dict
FinalDict = {}
count = 0
for k in sDict:
	if count >= ARGS_DIMENUME:
		break
	FinalDict[k[0]] = k[1]
	count += 1

# re-sort to ensure the order
fDict = sorted(FinalDict.items(), key=itemgetter(1), reverse=True)

# final serialize as dict
cPickle.dump(fDict, open(TARGETPATH,"wb"))

print "# done."