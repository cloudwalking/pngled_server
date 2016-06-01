#bin/python

import numpy
import serial
import time
from PIL import Image
from twisted.internet import reactor

class Player(object):
	def __init__(self, imagePath, frameOutClosure):
		self.imagePath = imagePath
		self.out = frameOutClosure
		self.fps = 30
		self.reloadImage()

	def reloadImage(self):
		print "reloading %s" % self.imagePath
		i = Image.open(self.imagePath).convert('RGB')
		self.image = numpy.asarray(i)
		print self.image.shape

	def step(self):
		now = time.time()
		frameNum = int ((now * self.fps) % self.image.shape[1])
		frame = self.image[::-1,frameNum,:]
		self.out(frame)

if __name__ == "__main__":
	filename = "white-150.png"
	port = serial.Serial('/dev/cu.usbserial-AD01V6V1', baudrate=9600)

	def frameOut(colors):
		port.write('\x60\x00')
		for color in colors:
			#port.write(chr(int(color[2])) + chr(int(color[0])) + chr(int(color[1])))
			print "%d %d %d" % (int(color[0]), int(color[1]), int(color[2]))
			port.write(chr(int(color[0])) + chr(int(color[1])) + chr(int(color[2])))
		port.flush()

	player = Player(filename, frameOut)

	def loop():
		player.step()
		reactor.callLater(0.01, loop)

	loop()
	reactor.run()
