#!/usr/bin/python3 -B
import itchat
import os
import time
	
f=open('/tmp/zzdoutput','r')
wxid=1000

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
	global f,wxid
	wx=msg['Text']
	os.system('echo %s >> /tmp/zzdwxin'%wx)
	while True:
		r=f.read()
		if r:
			break
		else:
			time.sleep(1)
	return r[4:]

def main():
	global f,wxid
	assert f
	r = f.readlines()
	r = r[-1]
	wxid=int(r[0:4])
	itchat.auto_login(True)
	itchat.run()
	f.close()

if __name__ == "__main__":
	main()
