import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import urllib2
from bs4 import BeautifulSoup

class rHandler(urllib2.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code ,msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)
		result.status = code
		result.headers = headers
		return result
	def http_error_302(self, req, fp, code, msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
		result.status = code
		result.headers = headers
		return result

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
PATH_UIDS   = 'uids/' + sys.argv[2]
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

# create necessary dir folder
os.mkdir("data/" + ARGS_STORE)
os.mkdir("freqs/" + ARGS_STORE)
os.mkdir("input_parts/" + ARGS_STORE)


#establish connection for each uid
for uid in ARGS_UIDS:
	#trim uid of '\n'
	uid = uid[0:10]
	#professional Weibo Handler - Redirect
	IS_PRO = False
	# init PATH
	PATH_REAL = "http://weibo.com/u/"+uid
	print '#debug: initLoc=%s' %PATH_REAL
	#open file for record storage, no / needed
	FP_STORE = open("data/"+ARGS_STORE+"/"+uid+".txt","w")
	try:
		for i in range(1,200):
			# 1st time request
			print "uid = %s, page = %s, 1st time" %(uid,str(i))
			# not or undefined
			if not IS_PRO:
				request = urllib2.Request(PATH_REAL+"?page="+str(i))
				opener = urllib2.build_opener(rHandler())
				request.add_header('Cookie',ARGS_COOKIE)
				# response = urllib2.urlopen(request)
				response = opener.open(request)
				# normal weibo
				if not hasattr(response,'status'):
					# notice: if 200, nothing will be set including the 'status' member
					pass
				# professional weibo
				elif response.status == 302 or response.status == 301:
					print "uid = %s, professional Weibo" %str(i)
					IS_PRO = True
					PATH_REAL = response.headers['Location']
					# complete some url
					if PATH_REAL.find("e.weibo.com") == -1:
						PATH_REAL = "http://e.weibo.com" + PATH_REAL
					print '#debug: Location=%s' %PATH_REAL
					#do the request again
					request = urllib2.Request(PATH_REAL+"?page="+str(i))
					# opener = urllib2.build_opener(rHandler())
					request.add_header('Cookie',ARGS_COOKIE)
					response = urllib2.urlopen(request)
					# response = opener.open(request)
				# unhandled type
				else:
					raise Exception,'MyCrawel: Invalid Return Code'
			# yes
			else:
				request = urllib2.Request(PATH_REAL+"?page="+str(i))
				# opener = urllib2.build_opener(rHandler())
				request.add_header('Cookie',ARGS_COOKIE)
				response = urllib2.urlopen(request)
			rawcontents = response.read()
			procontents = process_1(rawcontents)
			# -------- don't know why Professional Weibo FirstPage exit
			# judge to end first
			# if len(procontents) == 0:
				# break
			#----------------------------------------------------------
			FP_STORE.write(procontents)
			# fp.write('page #'+str(i)+' 1st:\n'+procontents+'\n')
			# print procontents
			# 2nd time request
			print "uid = %s, page = %s, 2nd time" %(uid,str(i))
			if IS_PRO:
				request = urllib2.Request("http://weibo.com/aj/mblog/mbloglist?uid="+uid+"&page="+str(i)+"&pagebar=0")
			else:
				request = urllib2.Request("http://e.weibo.com/aj/mblog/mbloglist?uid="+uid+"&page="+str(i)+"&pagebar=0")
			request.add_header('Cookie',ARGS_COOKIE)
			response = urllib2.urlopen(request)
			rawcontents = response.read()
			procontents = process_2(rawcontents)
			# judge to end first
			if len(procontents) == 0:
				break
			FP_STORE.write(procontents.decode('unicode-escape'))
			# fp.write('page #'+str(i)+' 2nd:\n'+procontents.decode('unicode-escape')+'\n')
			# 3rd time request
			print "uid = %s, page = %s, 3rd time" %(uid,str(i))
			if IS_PRO:
				request = urllib2.Request("http://weibo.com/aj/mblog/mbloglist?uid="+uid+"&page="+str(i)+"&pagebar=1")
			else:
				request = urllib2.Request("http://e.weibo.com/aj/mblog/mbloglist?uid="+uid+"&page="+str(i)+"&pagebar=1")
			request.add_header('Cookie',ARGS_COOKIE)
			response = urllib2.urlopen(request)
			rawcontents = response.read()
			procontents = process_2(rawcontents)
			# judge to end first
			if len(procontents) == 0:
				break
			FP_STORE.write(procontents.decode('unicode-escape'))
			# fp.write('page #'+str(i)+' 3rd:\n'+procontents.decode('unicode-escape')+'\n')
	except Exception,e:
		print e
		print "uid %s stop at page %s" %(uid,str(i))
		FP_STORE.close()
		continue
	FP_STORE.close()

print "Finished."