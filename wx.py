#!/usr/bin/python3 -B
import itchat
import os
import threading 
import time
	
pos = 0
getmess = False
nickname = '间'
user = None
username = None

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
	wx=msg['Text']
	if msg['User']['NickName'] != nickname:
		return '您好，我是人工智能小白...'
	else:
		os.system('echo %s >> /tmp/zzdwxin'%wx)
		return ''

def find_friend(nick_name):
	for friend in itchat.get_friends():
		if friend['NickName'] == nick_name:
			return friend

def get_message():
	global getmess,username,pos
	while getmess:
		f=open('/tmp/zzdoutput','r')
		f.seek(pos, 0)
		r=f.read()
		pos = f.tell()
		f.close()
		if r:
			print(r)
			itchat.send(msg=r[4:],toUserName=username)
		print('.')
		time.sleep(1)

def main():
	global pos,getmess
	global nickname,user,username
	
	f=open('/tmp/zzdoutput','r')
	r = f.read()
	pos = f.tell()
	f.close()
	print(r)
			
	itchat.auto_login(True)
	
	user = find_friend(nickname)
	username = user['UserName']

	getmess = True
	t = threading.Thread(target=get_message, args=())
	t.start()
	
	itchat.run()
	getmess = False
	t.wait()

if __name__ == "__main__":
	main()
