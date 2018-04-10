#!/usr/bin/python -B
# -*- coding: UTF-8 -*-
import sqlite3
import sys

def main():
	print('sql')
	conn = sqlite3.connect('./data/grammar.db')
	sql = u"select * from %s where name=\'%s\'"%(sys.argv[2].decode('utf8'), sys.argv[1].decode('utf8'))
	print sql
	cursor = conn.execute(sql)
	for c in cursor:
		for cc in c:
			print cc,
		print ''
	conn.close()

if __name__ == '__main__':
	main()
