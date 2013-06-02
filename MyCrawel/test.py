import re
# from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup

file_input = open("/home/chris/MyCrawel/testcases/test/input/case3.txt","r")
file_output = open("/home/chris/MyCrawel/testcases/test/output/case3.txt","w")

cts = ""
#read content
while 1:
	line = file_input.readline()
	if not line:
		break
	cts += line

#step1
start_1 = cts.find('</body>')+7
end_1 = cts.find('</html>')
cts_1 = cts[start_1:end_1]

#step2
_start_2 = cts_1.find('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_content_hisFeed"')
start_2 = cts_1.find('"html"',_start_2) + 8
end_2 = cts_1.find('</script>',_start_2) - 2
cts_2 = cts_1[start_2:end_2]

#step3
cts_3 = cts_2
cts_3 = cts_3.replace("\\t","\t")
cts_3 = cts_3.replace("\\r\\n","")
cts_3 = cts_3.replace("\\/","/")
cts_3 = cts_3.replace('\\"','"')

#load
fakeHead = """<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>Fake Title</title></head><body>"""
fakeTail = """</body></html>"""
# cts_4 = fakeHead + cts_3 + fakeTail
pattern = re.compile(r'<div class="WB_text".+?</div>')
cts_4 = pattern.findall(cts_3)
cts_5 = fakeHead + ''.join(cts_4) + fakeTail

soup = BeautifulSoup(cts_5)
cts_6 = soup.select(".WB_text")

#put
rawchars = ""
for k in cts_6:
	for j in k.children:
		if j.find("</a>") == -1:
			rawchars += j

print rawchars



#test
fp = open("/home/chris/temporary.txt","w")
fp.write('\n'.join(cts_4))
fp.close()

# soup = BeautifulSoup(cts)
# divs = soup.select("#pl_content_top")
# print divs
# print str(soup.findall("a"))
# for k in divs:
# 	print k.contents


# #pattern!
# pattern = re.compile('\\\\u....')
# match = pattern.findall(line)
# #transfer!
# for k in match:
# 	contents += unichr(int(k[2:],16))

# print contents