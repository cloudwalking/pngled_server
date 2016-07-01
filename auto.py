#bin/python

pixel_count = 288

import numpy
import os
import serial
import time
from neopixel import *
from PIL import Image
from twisted.internet import reactor

class Player(object):
	def __init__(self, frameOutClosure):
		self.out = frameOutClosure
		self.fps = 30

	def load(self, imagePath):
		print "reloading %s" % imagePath
		i = Image.open(imagePath).convert('RGB')
		self.image = numpy.asarray(i)

	def step(self):
		if not hasattr(self, "image"):
			return
		now = time.time()
		frameNum = int ((now * self.fps) % self.image.shape[1])
		frame = self.image[::-1,frameNum,:]
		self.out(frame)

class Strip(object):
	def __init__(self, numPixels, brightness):
		self.numPixels = numPixels
		self.leds = Adafruit_NeoPixel(numPixels, 18, 800000, 5, False, brightness)
		self.leds.begin()
		self.clear()
	
	def clear(self):
		for x in xrange(self.numPixels):
			self.leds.setPixelColor(x, Color(0, 0, 0))
		self.leds.show()

	def showFrame(self, colors):
		i = 0
		for color in colors:
			# Don't address pixels beyond our strip.
			if i > self.numPixels:
				break
			r = int(color[1])
			g = int(color[0])
			b = int(color[2])
			color = Color(r, g, b)
			self.leds.setPixelColor(i, color)
			i += 1
		self.leds.show()


if __name__ == "__main__":
	
	strip = Strip(pixel_count, 100)

	def frameOut(colors):
		strip.showFrame(colors)

	player = Player(frameOut)

	def findFile():
		#filename = file_name
		dir = os.path.dirname(__file__)
		names = os.listdir(".")
		files = [(os.path.getmtime(f), f) for f in names if f.endswith(".png")]
		files.sort()
		filename = files[-1][1]
		filepath = os.path.join(dir, filename)
		return filepath
	
	def reloadLoop():
		player.load(findFile())
		reactor.callLater(10.0, reloadLoop)
	
	reloadLoop()

	def loop():
		player.step()
		reactor.callLater(0.01, loop)

	loop()
	reactor.run()
