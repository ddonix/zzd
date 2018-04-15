#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wave
import os
import subprocess
import mp3play

def main():
	playmusic(sys.argv[1])

def mp():
	f = open('/tmp/mfifo','w+')
	print f
	f.write('pause\n')
	f.close()

def playmusic(path):
	clip = mp3play.load(path)
	clip.play()
	time.sleep(10)   
	clip.stop()
	playmusic()

if __name__ == '__main__':
	main()

