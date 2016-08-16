#!/usr/bin/python

import sys, os
import cv2
import numpy

slice_x = 50
slice_width = 1

def main(argv):
  inputfile = "x.mp4"

  path = os.path.abspath(os.path.expanduser(inputfile))
  print path

  capture = cv2.VideoCapture(path)
  outimage = None
  
  while (True):
    ret, frame = capture.read()
    if ret == False:
      break

    crop = frame[0:720, slice_x:slice_x + slice_width]

    if outimage == None:
      outimage = crop
    else:
      outimage = numpy.concatenate((outimage, crop), axis = 1)

  capture.release()

  outpath = "%.jpg"%inputfile
  cv2.imwrite(outpath, outimage)

if __name__ == "__main__":
   main(sys.argv[1:])
