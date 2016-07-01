#bin/python

pixel_count = 338 
file_name = "led-feast-27.png"
default_brightness = 250

import numpy
import os
import serial
import time
import sys
from neopixel import *
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

	def step(self):
		now = time.time()
		frameNum = int((now * self.fps) % self.image.shape[1])
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
			# Skip every other pixel for power savings.
			#if i % 2 == 0:
			#	i += 1
			#	continue
			r = int(color[1])
			g = int(color[0])
			b = int(color[2])
			color = Color(r, g, b)
			self.leds.setPixelColor(i, color)
			i += 1
		self.leds.show()


if __name__ == "__main__":
	filename = file_name
	if len(sys.argv) > 1:
		filename = sys.argv[1]	
	dir = os.path.dirname(__file__)
	filepath = os.path.join(dir, filename)
	
	strip = Strip(pixel_count, default_brightness)

	def frameOut(colors):
		strip.showFrame(colors)

	player = Player(filepath, frameOut)

	def loop():
		player.step()
		reactor.callLater(0.01, loop)

	loop()
	reactor.run()
