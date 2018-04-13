class database:
	_gset_all = {}
	_spbase_all = {}
	_table_vocable = {u' '}
	_identifyDict = {}
	_defineDict = {}
	_keyword_zzd = {}

	@classmethod
	def gsetinit(cls):
		conn = sqlite3.connect('./data/grammar.db')
		cursor = conn.execute("select * from gset_phrase")
		v = cursor.fetchall()
		cursor = conn.execute("select * from gset_sentence")
		v.extend(cursor.fetchall())
		conn.close()
		while v != []:
			if v[0][0] in cls._gset_all:
				v.pop(0)
				continue
			skip = True
			for g in v[0][1:]:
				if g == '' or g == None or (g in cls._gset_all):
					continue
				if not (g[0] == u'[' and g[-1] == u']'):
					break
				if not u'|' in g:
					gsp = g[1:-1].split(' ')
					skip2 = True
					for gg in gsp:
						if gg == '' or gg == u'...' or gg[0] == u's' or gg[0:2] == u'ws' or (gg in cls._gset_all):
							continue
						if gg[0] == u'p' and gg[1:] in cls._gset_all:
							continue
						if gg[0] == u'w' and gg[1:] in cls._gset_all:
							continue
						print u'依赖%s'%gg
						break
					else:
						skip2 = False
					if skip2:
						break
				else:
					gsp = g[1:-1].split('|')
					skip2 = True
					for gg in gsp[1:]:
						if not (gg == '' or (gg in cls._gset_all)):
							break
					else:
						skip2 = False
					if skip2:
						break
			else:
				gset(v[0][0], v[0][1:])
				v.pop(0)
				skip = False
			if skip:
				tmp = v.pop(0)
				v.append(tmp)
		for name in cls._gset_all:
			print name, len(cls._gset_all[name].child)

	@classmethod
	def spinit(cls):
		conn = sqlite3.connect('./data/grammar.db')
		cursor = conn.execute("select * from cls._table_vocable")
		cls._table_vocable = set()
		for v in cursor:
			assert len(v[0]) == 1
			sp = sentencephrase(v)
			cls._spbase_all[v[0]] = {v[0]:sp}
			cls._table_vocable.add(v[0])
		sp = sentencephrase((u' ', u'空格'))
		cls._spbase_all[u' '] = {u' ':sp}
	
		cursor = conn.execute("select * from table_phrase")
		for v in cursor:
			assert len(v[0]) > 1
			for i in v[0]:
				if not i in cls._spbase_all:
					print '在词组表中出现的字符没有在字符表中出现',v[0],i
				assert i in cls._spbase_all
			sp = sentencephrase(v)
			cls._spbase_all[v[0][0]][v[0]] = sp
		conn.close()
	
	@classmethod
	def coreinit(cls):
		conn = sqlite3.connect('./data/grammar.db')
		cursor = conn.execute("select * from define")
		for define in cursor:
			cls._defineDict[define[0]] = define[1]
			for defi in define:
				for d in defi:
					if not d in cls._table_vocable:
						print '定义中没有在字符表中出现的字符',defi, d
					assert d in cls._table_vocable

		
		cursor = conn.execute("select * from zzd_keyword")
		for keyword in cursor:
			cls._keyword_zzd[keyword[0]] = keyword[1:]
		
		for sp in cls._spbase_all:
			for s in cls._spbase_all[sp]:
				if cls._spbase_all[sp][s].be(u'zzd关键字'):
					if not s in cls._keyword_zzd:
						print '在符号表中定义为zzd关键字，但是没有在关键字表中出现',s
					assert s in cls._keyword_zzd

		cursor = conn.execute("select * from verify")
		for guest in cursor:
			cls._identifyDict[guest[0]] = guest[1]
		conn.close()
