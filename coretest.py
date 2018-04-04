#!/usr/bin/python -B
# -*- coding: UTF-8 -*-

import zzd_core0
import xlrd
#init:初始化。
#stand：完成一次交互，等待下一次交互。没有预期。
#wait:期待human的回应。有预期。
#initiative:主动状态，主动发起对话。
STATE = ('init', 'stand', 'wait', 'initiative')

#0:工作模式；1:娱乐模式;2:训练模式;3:调试模式.
MODE = ('work', 'train', 'debug')

class zzdcore1:
	inWaaClass = []		#输入语句类型
	defineDict = {}
	grammar_vocable = []
	grammar_phrase = []
	grammar_sentence = []
	tabel_vocable = []
	tabel_phrase = []
	tabel_sentence = []

	def __init__(self, corelayer0):
		self.sentence = []
		self.corelayer0 = corelayer0
		self.state = 'init'
		self.mode = 'work'
		self.friend = None
	
	@classmethod
	def init(cls):
		zzd_core0.zzdcore0.init()
		
		xlsfile = r"txt/gramma.xls"# 打开指定路径中的xls文件
		book = xlrd.open_workbook(xlsfile)#得到Excel文件的book对象，实例化对象
		sheet0 = book.sheet_by_index(0) # 通过sheet索引获得sheet对象
		print "1、",sheet0
	
def main():
	print('hello')
	core0 = zzd_core0.zzdcore0()
	zzdcore1.init()
	core1 = zzdcore1(core0)

if __name__ == '__main__':
	main()
