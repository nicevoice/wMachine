import time
import thread
import subprocess
from select import select
from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS

isread = False
isprun = False
strout = ""
p = None

def fetchResult():
	global strout
	global isread
	global isprun
	# data=p.stdout.readline()
	data = ""
	while 1:
		# print data
		# print "#judge%s"%isread
		# print "#strout=%s"%strout
		# if isread:
		# 	isread = False
		# 	strout = ""
		if isprun:
			strout += data
			data = ""
			try:
				il, ol, el = select([p.stdout],[],[],2)
			except AttributeError, e:
				pass
			except Exception, e:
				strout += "# Unknown Error 2, Enter 'kill' to Reset."
			for s in il:
				data = s.readline()
			# data=p.stdout.readline()
			print "####second readline####"

def setFlag():
	global isread
	global isprun
	global strout
	global p
	while 1:
		if isread:
			isread = False
			strout = ""
		if p != None:
			ret = subprocess.Popen.poll(p)
			if ret is None:
				isprun = True
			else:
				print "#poll is not None"
				isprun = False
				try:
					p.kill()
				except OSError,e:
					pass
				except Exception,e:
					strout += "# Unknown Error 1. Enter 'kill' to Reset."
				p = None
		# time.sleep(0.1)

# trueout = ""

class EchoServerProtocol(WebSocketServerProtocol):
	def onMessage(self, msg, binary):
		global p
		global isread
		global isprun
		global strout
		print "#recv:%s"%msg
		# kill the process
		if msg == "kill":
			if isprun:
				p.kill()
				isprun = False
				strout += "# Process Killed.\n"
				p = None
			else:
				strout += "# No Process Running.\n"
			# self.sendMessage(strout, binary)
			# isread = True
		elif msg == "query":
			self.sendMessage(strout, binary)
			isread = True
			# print "#recv!True"
			# print "#recv:%s"%msg
		else:
			if isprun:
				strout += "# A process is already running. Send 'kill' to terminate it before you start another one.\n"
			else:
				params = ['python','-u'] + msg.split(' ')
				try:
					p=subprocess.Popen(params, shell=False, stdout=subprocess.PIPE)
				except Exception, e:
					strout += "# Unrecognized Command. Enter 'kill' to Reset."
			# self.sendMessage(strout, binary)
			# isread = True



thread.start_new_thread(setFlag,())
thread.start_new_thread(fetchResult,())

factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
factory.protocol = EchoServerProtocol
listenWS(factory)
reactor.run()