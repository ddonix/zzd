#!/usr/bin/python3 -B
import itchat
import os

f=open('/tmp/zzdfifo','r')
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
	global f
	wx=msg['Text']
	os.system('echo %s >> /tmp/zzdwx'%wx)
	r=f.read()
	return 'zzd:%s'%r

def find_friend(nick_name):
	for friend in itchat.get_friends():
		if friend['NickName'] == nick_name:
			return friend
			
def main():
	os.system('rm /tmp/zzdwx -f')
	os.system('mkfifo /tmp/zzdwx')
	itchat.auto_login(True)
	itchat.run()

if __name__ == "__main__":
	main()
