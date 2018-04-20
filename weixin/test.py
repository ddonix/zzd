#!/usr/bin/python3 -B
import itchat

def find_friend(nick_name):
	for friend in itchat.get_friends():
		if friend['NickName'] == nick_name:
			return friend
			
def main():
	itchat.auto_login(True)
	friend = find_friend('王燕妮')
	username = friend['UserName']
	itchat.send(msg='您好，这是来自人工智障小冬的问候!',toUserName=username)
	itchat.logout()

if __name__ == "__main__":
	main()
