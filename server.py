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
		i = Image.open(self.imagePath)
		self.image = numpy.asarray(i)
		print self.image.shape

	def step(self):
		now = time.time()
		frameNum = int ((now * self.fps) % self.image.shape[1])
		frame = self.image[::-1,frameNum,:]
		self.out(frame)

if __name__ == "__main__":
	filename = "rainbow-test.png"
	port = serial.Serial('/dev/tty.usbserial-AD01V6V1', baudrate=115200)

	# Allow Arduino to reset.
	time.sleep(2)

	def frameOut(colors):
		port.write('\x60\x00')
		for color in colors:
			port.write(chr(int(color[2])) + chr(int(color[0])) + chr(int(color[1])))
		port.flush()

	player = Player(filename, frameOut)

	def loop():
		player.step()
		reactor.callLater(0.01, loop)

	loop()
	reactor.run()
