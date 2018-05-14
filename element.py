#!/usr/bin/python3 -B
class phbase:
    def __init__(self, kdb, s):
        assert type(s) == str
        self.s = s                #sting
        self.gs = set()
        self.fn = {}
        self.kdb = kdb
    
    def addfn(self, fn):
        fn = fn.split('~')
        for f in fn:
            name,value=f.split(':')
            self.fn[name]=value
        print(self.fn)
    
    def _addgs(self, gs):
        if gs not in self.gs:
            self.gs.add(gs)
    
    def _removegs(self, gs):
        assert gs in self.gs
        self.gs.remove(gs)
    
class seph:
    def __init__(self, kdb, s):
        assert type(s) == str
        self.s = s                #sting
        self.d = []
        self.gs = set()
        self.fn = {}
        self.kdb = kdb
    
    def _fenci(self, point=False):
        znumber =  '0123456789'
        cnumber =  '零一二三四五六七八九十百千万亿'
        zstr = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        zpoint = '，。,.！!？?'
        if self.kdb.spin(self.s):
            self.d.append(self)
            return
        for name in ['数','汉语数','字符串']:
            gs = self.kdb.getgs(name)
            if gs.judge1(self)[0] == True:
                self._addgs(gs)
                self.d.append(self)
                return
        
        ss = self.s
        while ss != '':
            if ss[0] == ' ':
                ss = ss[1:]
            elif ss[0] in znumber:
                s = ss[0]
                ss = ss[1:]
                while ss != '' and ss[0] in znumber:
                    s += ss[0]
                    ss = ss[1:]
                sp = seph(self.kdb, s)
                sp._addgs(self.kdb.getgs('数'))
                self.d.append(sp)
            elif ss[0] in zstr[10:]:
                s = ss[0]
                ss = ss[1:]
                while ss != '' and ss[0] in zstr:
                    s += ss[0]
                    ss = ss[1:]
                sp = seph(self.kdb, s)
                sp._addgs(self.kdb.getgs('字符串'))
                self.d.append(sp)
            elif ss[0:2] == '!=':
                self.d.append(self.kdb.getsp('!='))
                ss = ss[2:]
            elif ss[0:2] == '>=':
                self.d.append(self.kdb.getsp('>='))
                ss = ss[2:]
            elif ss[0:2] == '<=':
                self.d.append(self.kdb.getsp('<='))
                ss = ss[2:]
            elif ss[0] in zpoint:
                if point:
                    self.d.append(self.kdb.getsp(ss[0]))
                ss = ss[1:]
            else:
                for i in range(min(8,len(ss)),1,-1):
                    if self.kdb.spin(ss[0:i]):
                        if self.kdb.getsp(ss[0:i]) == self:
                            continue
                        self.d.append(self.kdb.getsp(ss[0:i]))
                        ss = ss[i:]
                        break
                else:
                    if ss[0] not in cnumber:
                        assert self.kdb.spin(ss[0])
                        self.d.append(self.kdb.getsp(ss[0]))
                        ss = ss[1:]
                    else:
                        s = ss[0]
                        ss = ss[1:]
                        while ss != '' and ss[0] in cnumber:
                            s += ss[0]
                            ss = ss[1:]
                        sp = seph(self.kdb, s)
                        sp._addgs(self.kdb.getgs('汉语数'))
                        self.d.append(sp)
    
    def addfn(self, fn):
        fn = fn.split('~')
        for f in fn:
            name,value=f.split(':')
            self.fn[name]=value
        print(self.fn)
    
    def _addgs(self, gs):
        if gs not in self.gs:
            self.gs.add(gs)
    
    def _removegs(self, gs):
        assert gs in self.gs
        self.gs.remove(gs)
    
    #0:是
    #1:不是
    #2:不确定
    def be(self, gram):
        if not self.kdb.gsin(gram):
            return [2,'%s:不是已知的集合或者函数'%gram]
        gs = self.kdb.getgs(gram)
        if gram == '集合':
            return gs.judge2(self)
        else:
            return gs.judge1(self)
            
def main():
    print('element')
    
if __name__ == '__main__':
    main()
            
def main():
    print('element')
    
if __name__ == '__main__':
    main()
