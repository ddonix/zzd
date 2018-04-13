
	def _fensp(self, phrases, mend):
		if phrases == []:
			if not mend:
				return None
			else:
				if self.name == u'句号':
					phrases.insert(0,database.sp(u'。'))
				elif self.name == u'感叹号':
					phrases.insert(0,database.sp(u'！'))
				elif self.name == u'问号':
					phrases.insert(0,database.sp(u'？'))
				elif self.name == u'下引号':
					phrases.insert(0,database.sp(u'”'))
				else:
					return None
				return (phrases[0], [], {})
		if self.child != []:
			ress = []
			for i in range(-1,-len(self.child)-1, -1):
				res = self.child[i]._fensp(phrases, mend)
				if res:
					res[2][self.name] = res[0].s
					ress.append(res)
					return res
		else:
			if self.name[0] == '[' and self.name[-1] == u']':
				frame = self.name[1:-1].split(u' ')
			else:
				frame = []
			key = {}
			if frame == []:
				if phrases[0].be(self.name):
					key[self.name] = phrases[0].s
					return (database.sp(phrases[0]), phrases[1:], key)
				else:
					if mend:
						if self.name == u'逗号':
								phrases.insert(0,database.sp(u'，'))
						elif self.name == u'句号':
								phrases.insert(0,database.sp(u'。'))
						elif self.name == u'感叹号':
								phrases.insert(0,database.sp(u'！'))
						elif self.name == u'问号':
								phrases.insert(0,database.sp(u'？'))
						elif self.name == u'上引号':
								phrases.insert(0,database.sp(u'“'))
						else:
							return None
						return (phrases[0], phrases[1:], key)
					return None
			else:
				ress = []
				for i, gram in enumerate(frame):
					if gram == '':
						continue
					if gram in gset_all:
						g = gset_all[gram]
						res = g._fensp(phrases, mend)
						if res == None:
							return None
						key[g.name] = res[0].s
						for k in res[2]:
							key[k] = res[2][k]
						ress.append(res)
						phrases = res[1]
					else:
						if gram == u'...':
							if i < len(frame)-1:
								while not (phrases[0].be(frame[i+1])):
									ress.append((database.sp(phrases[0]), phrases[1:], {}))
									phrases = phrases[1:]
									if phrases == []:
										break
							else:
								if phrases == []:
									break
								while True:
									ress.append((database.sp(phrases[0]), phrases[1:], {}))
									phrases = phrases[1:]
									if phrases == []:
										break
						elif gram[0] == u's':
							if phrases[0].s == gram[1:]:
								ress.append((database.sp(phrases[0]), phrases[1:], {}))
								phrases = phrases[1:]
							else:
								return None
						elif gram[0:2] == u'ws':
							if phrases[0].s == gram[2:]:
								ress.append((database.sp(phrases[0]), phrases[1:], {}))
								phrases = phrases[1:]
							else:
								if mend:
									ress.append((database.sp(gram[2:]), phrases, {}))
								else:
									continue
						elif gram[0] == u'w':
							assert gram[1:] in gset_all
							g = gset_all[gram[1:]]
							res = g._fensp(phrases, mend)
							if res != None:
								key[g.name] = res[0].s
								for k in res[2]:
									key[k] = res[2][k]
								ress.append(res)
								phrases = res[1]
							else:
								if mend and len(g.sp) == 1:
									for ph in g.sp:
										ress.append((ph, phrases, {}))
										break
								else:
									continue
						else:
							return None
				sps = []
				for res in ress:
					sps.append(res[0])
				sp = database.sp(sps, self)
				key[self.name] = sp.s
				return (sp, ress[-1][1], key)
