import time
import thread
from subprocess import *
from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS

def fetchResult():
	while data:
		# print data
		strout += data
		data=p.stdout.readline()
	p.kill()

p=Popen(['python','-u','CalcFreq.py','caijing'],shell=False,stdout=PIPE)
strout = ""
# trueout = ""

class EchoServerProtocol(WebSocketServerProtocol):
	def onMessage(self, msg, binary):
		self.sendMessage(strout, binary)
		# strout = ""
		# if msg == 'abc':
		# 	self.sendMessage('YES',binary)
		# self.sendMessage(msg, binary)


if __name__ == '__main__':
	factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
	factory.protocol = EchoServerProtocol
	listenWS(factory)
	reactor.run()