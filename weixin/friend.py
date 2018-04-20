#!/usr/bin/python3 -B
import itchat

def all_friend():
	friends = itchat.get_friends()
	for friend in friends:
		print('NikeName: %s'%friend['NickName'])
			
def main():
	itchat.auto_login(True)
	all_friend()
	itchat.logout()

if __name__ == "__main__":
	main()
