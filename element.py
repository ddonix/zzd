#!/usr/bin/python3 -B
class phrases:
    def __init__(self, s):
        assert type(s) == str
        self.s = s                #sting
        self.gs = set()
        self.fn = {}
    
    @classmethod
    def init(cls, kdb):
        cls.kdb = kdb
    
    def addfn(self, fn):
        fn = fn.split('~')
        for f in fn:
            name,value=f.split(':')
            self.fn[name]=value
    
    def _addgs(self, gs):
        if gs not in self.gs:
            self.gs.add(gs)
    
    def be(self, gram):
        gs = phrases.kdb.getgs(gram)
        if not gs:
            return (2,'%s:不是已知的集合'%gram)
        if phrases.kdb.getgs('集合') in self.gs:
            return gs.judge2(self)
        else:
            return gs.judge1(self)
    
    def affirm(self, gram):
        gs = phrases.kdb.getgs(gram)
        if not gs:
            return (2,'%s:不是已知的集合'%gram)
        if phrases.kdb.getgs('集合') not in self.gs:
            res = gs.affirm1(self)
            if res[0] == True:
                self._addgs(gs)
            return res
        else:
            child = phrases.kdb.getgs(self.s)
            res = gs.affirm2(child)
            if res[0] == True:
                child.father.append(ds)
            return res
    
class sentence:
    def __init__(self, kdb, s):
        assert type(s) == str
        self.s = s                #sting
        self.ph = []
        self.kdb = kdb
        zpoint = '，。,.！!？?'
        ss = self.s
        while ss:
            if ss[0] == ' ':
                ss = ss[1:]
                continue
            for i in range(min(12,len(ss)),1,-1):
                ph = self.kdb.getph(ss[0:i])
                if ph:
                    self.ph.append(ph)
                    ss = ss[i:]
                    break
            else:
                if ss[0] in zpoint:
                    ss = ss[1:]
                else:
                    ph = self.kdb.getph(ss[0])
                    assert ph
                    self.ph.append(ph)
                    ss = ss[1:]
    
    #0:是
    #1:不是
    #2:不确定
    def be(self, gram):
        gs = self.kdb.getgs(gram)
        if not gs:
            return [2,'%s:不是已知的集合或者函数'%gram]
        res = self.kdb.getgs('集合').judge1(self)
        if res[0] == True:
            if gram == '集合':
                return (True, self.kdb.getgs('集合'))
            else:
                return gs.judge2(self.kdb.getgs(self.s))
        else:
            return gs.judge3(self)

def main():
    print('element')
    
if __name__ == '__main__':
    main()
