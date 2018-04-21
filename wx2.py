#!/usr/bin/python3 -B
import itchat
import os
import time
	
f=open('/tmp/zzdfifo','r')
def main():
	global f
	os.system('rm /tmp/zzdwx -f')
	os.system('mkfifo /tmp/zzdwx')
	r = f.readlines()
	r = r[-1]
	print(r)

if __name__ == "__main__":
	main()
