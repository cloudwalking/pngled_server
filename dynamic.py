#bin/python

pixel_count = 288

import numpy
import os
import serial
import time
import urllib
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

	def getRemoteImageURL():
		response = urllib.urlopen('http://pilot-lightstick.appspot.com/now')
		imgurl = response.read()
		return imgurl
	
	currentImageURL = None

	def reloadLoop():
		remoteImageURL = getRemoteImageURL()
		global currentImageURL
		if currentImageURL != remoteImageURL:
			currentImageURL = remoteImageURL
			urllib.urlretrieve(currentImageURL, 'animation.png')
			player.load('animation.png')
		reactor.callLater(2.0, reloadLoop)
	
	reloadLoop()

	def loop():
		player.step()
		reactor.callLater(0.01, loop)

	loop()
	reactor.run()
