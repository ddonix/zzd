#!/usr/bin/python 
# -*- coding:utf-8 -*- 
import zzd_unity
import xlrd

class human(zzd_unity.unity):
	table_vocable = None
	def __init__(self):
		zzd_unity.unity.__init__(self)
		self.waalist = []
    
	@classmethod
	def init(cls):
		xlsfile = r"data/grammar.xls"		# 打开指定路径中的xls文件
		book = xlrd.open_workbook(xlsfile)	#得到Excel文件的book对象，实例化对象
		# 通过sheet名字来获取，当然如果知道sheet名字就可以直接指定
		sheet = book.sheet_by_name('allow')
		human.table_vocable = u'0123456789'+u''.join(sheet.col_values(0))
		book.release_resources()
		print human.table_vocable

	def act(self, dest, waa_out):
		res = dest.echo(self, waa_out)
		self.waalist.append([waa_out, res])
		return None
	
	def echo(self, sour, waa_in):
		raise NotImplementedError
    
	def forword(self, dest, waa_out):
		return waa_out
