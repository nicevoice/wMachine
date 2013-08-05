import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import urllib2
from bs4 import BeautifulSoup

#deal with first time fetch contents
def process_1(rts):
	#step1
	start_1 = rts.find('</body>') + 7
	end_1 = rts.find('</html>')
	rts_1 = rts[start_1:end_1]
	#step2
	_start_2 = rts_1.find('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_content_hisFeed"')
	start_2 = rts_1.find('"html',_start_2) + 8
	end_2 = rts_1.find('</script>',_start_2) - 2
	rts_2 = rts_1[start_2:end_2]
	#step3
	rts_3 = rts_2
	rts_3 = rts_3.replace("\\t","\t")
	rts_3 = rts_3.replace("\\r\\n","")
	rts_3 = rts_3.replace("\\/","/")
	rts_3 = rts_3.replace('\\"','"')
	#step4
	fakeHead = """<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>Fake Title</title></head><body>"""
	fakeTail = """</body></html>"""
	pattern = re.compile(r'<div class="WB_text".+?</div>')
	rts_4 = pattern.findall(rts_3)
	rts_5 = fakeHead + ''.join(rts_4) + fakeTail
	#step5
	soup = BeautifulSoup(rts_5)
	rts_6 = soup.select(".WB_text")
	#step6 - put
	rawchars = ""
	for k in rts_6:
		for j in k.children:
			if j.find("</a>") == -1:
				rawchars += j
	return rawchars

#deal with second and third time request
def process_2(rts):
	#step1
	rts_1 = rts
	#step2
	# _start_2 = rts_1.find('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_content_hisFeed"')
	start_2 = rts_1.find('"html') + 8
	# end_2 = rts_1.find('</script>',_start_2) - 2
	rts_2 = rts_1[start_2:]
	#step3
	rts_3 = rts_2
	rts_3 = rts_3.replace("\\t","\t")
	rts_3 = rts_3.replace("\\r\\n","")
	rts_3 = rts_3.replace("\\/","/")
	rts_3 = rts_3.replace('\\"','"')
	#step4
	fakeHead = """<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>Fake Title</title></head><body>"""
	fakeTail = """</body></html>"""
	pattern = re.compile(r'<div class="WB_text".+?</div>')
	rts_4 = pattern.findall(rts_3)
	rts_5 = fakeHead + ''.join(rts_4) + fakeTail
	#step5
	soup = BeautifulSoup(rts_5)
	rts_6 = soup.select(".WB_text")
	#step6 - put
	rawchars = ""
	for k in rts_6:
		for j in k.children:
			if j.find("</a>") == -1:
				rawchars += j
	return rawchars

#paths
PATH_COOKIE = sys.argv[1]
PATH_UIDS   = sys.argv[2]
PATH_STORE  = sys.argv[3]

#arguments
ARGS_COOKIE = ""
ARGS_UIDS   = []
ARGS_STORE  = PATH_STORE

#read cookie - one line
FP_COOKIE = open(PATH_COOKIE,"r")
ARGS_COOKIE = FP_COOKIE.readline()
FP_COOKIE.close()

#read uids - multiple line
FP_UIDS = open(PATH_UIDS,"r")
while 1:
	line = FP_UIDS.readline()
	if not line:
		break
	ARGS_UIDS.append(line)
FP_UIDS.close()

#-------------------------test
# fp = open("./log.txt","w")
#-------------------------test



#establish connection for each uid
for uid in ARGS_UIDS:
	#trim uid of '\n'
	uid = uid[0:-1]
	#open file for record storage, no / needed
	FP_STORE = open("data/"+ARGS_STORE+"/"+uid+".txt","w")
	try:
		for i in range(1,100):
			# 1st time request
			print "uid = %s, page = %s, 1st time" %(uid,str(i))
			request = urllib2.Request("http://weibo.com/u/"+uid+"?page="+str(i))
			request.add_header('Cookie',ARGS_COOKIE)
			response = urllib2.urlopen(request)
			rawcontents = response.read()
			procontents = process_1(rawcontents)
			FP_STORE.write(procontents)
			# fp.write('page #'+str(i)+' 1st:\n'+procontents+'\n')
			# print procontents
			# 2nd time request
			print "uid = %s, page = %s, 2nd time" %(uid,str(i))
			request = urllib2.Request("http://weibo.com/aj/mblog/mbloglist?uid="+uid+"&pre_page="+str(i)+"&pagebar=0")
			request.add_header('Cookie',ARGS_COOKIE)
			response = urllib2.urlopen(request)
			rawcontents = response.read()
			procontents = process_2(rawcontents)
			FP_STORE.write(procontents.decode('unicode-escape'))
			# fp.write('page #'+str(i)+' 2nd:\n'+procontents.decode('unicode-escape')+'\n')
			# 3rd time request
			print "uid = %s, page = %s, 3rd time" %(uid,str(i))
			request = urllib2.Request("http://weibo.com/aj/mblog/mbloglist?uid="+uid+"&pre_page="+str(i)+"&pagebar=1")
			request.add_header('Cookie',ARGS_COOKIE)
			response = urllib2.urlopen(request)
			rawcontents = response.read()
			procontents = process_2(rawcontents)
			FP_STORE.write(procontents.decode('unicode-escape'))
			# fp.write('page #'+str(i)+' 3rd:\n'+procontents.decode('unicode-escape')+'\n')
	except Exception,e:
		print e
		print "uid %s stop at page %s" %(uid,str(i))
		FP_STORE.close()
		continue
	FP_STORE.close()

print "Finished."