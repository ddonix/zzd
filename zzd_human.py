#!/usr/bin/python 
# -*- coding:utf-8 -*- 
import unity
import xlrd

class human(unity.unity):
	table_vocable = None
	def __init__(self):
		unity.unity.__init__(self)
		self.waalist = []
    
	@classmethod
	def init(cls):
		xlsfile = r"txt/grammar.xls"		# 打开指定路径中的xls文件
		book = xlrd.open_workbook(xlsfile)	#得到Excel文件的book对象，实例化对象
		# 通过sheet名字来获取，当然如果知道sheet名字就可以直接指定
		sheet = book.sheet_by_name('grammar_vocable')
		tmp = u''.join(sheet.col_values(2))
		book.release_resources()
		tmp = set(tmp)
		human.table_vocable = u''
		for item in tmp:
			human.table_vocable += item

	def act(self, dest, waa_out):
		res = dest.echo(self, waa_out)
		self.waalist.append([waa_out, res])
		return None
	
	def echo(self, sour, waa_in):
		raise NotImplementedError
    
	def forword(self, dest, waa_out):
		return waa_out
