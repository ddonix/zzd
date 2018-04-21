#!/usr/bin/python3 -B
import os
import time

def main():
	os.system('rm /tmp/zzdwx -f')
	os.system('mkfifo /tmp/zzdwx')
	f=open('/tmp/zzdfifo','r')
	while True:
		r=f.readline()
		if r:
			print(r)
		else:
			time.sleep(1)

if __name__ == "__main__":
	main()
