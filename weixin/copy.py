#!/usr/bin/python3 -B
import itchat

'''
@itchat.msg_register
def simple_reply(msg):
  if msg['Type'] == TEXT:
      return 'I received: %s' % msg['Content']
'''	   

def find_friend(nick_name):
	for friend in itchat.get_friends():
		if friend['NickName'] == nick_name:
			return friend
			
def main():
	itchat.auto_login(True)
	friend = find_friend('冬')
	username = friend['UserName']
	itchat.send(msg='您好，这是来自人工智障小冬的问候!进入复制模式。',toUserName=username)
	itchat.run()

if __name__ == "__main__":
	main()
