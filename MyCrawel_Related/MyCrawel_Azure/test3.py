import itemgetter
import jieba
import jieba.posseg as pseg
jieba.load_userdict("/home/chris/MyCrawel/dicts/0.txt")
jieba.load_userdict("/home/chris/MyCrawel/dicts/1.txt")
jieba.load_userdict("/home/chris/MyCrawel/dicts/2.txt")
jieba.load_userdict("/home/chris/MyCrawel/dicts/3.txt")
jieba.load_userdict("/home/chris/MyCrawel/dicts/4.txt")
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

fp = open("/home/chris/MyCrawel/data/caijing/1032648501.txt","r")
contents = ""
while 1:
	line = fp.readline()
	if not line:
		break
	contents += line

fp.close()

MyDict = {}

res = pseg.cut(contents)
for w in res:
	if not MyDict.has_key(w.word):
		MyDict[w.word] = 1
	else:
		MyDict[w.word] += 1

#sort
sDict = sorted(MyDict.items(), key=itemgetter(1), reverse=True)


for k in sDict:
	print "%s,%s" %(k[0],k[1])
