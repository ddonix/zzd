#!/usr/bin/python3 -B
import element
class fn:
    def __init__(self, gfunc, d, v, f):
        assert gfunc
        
        self.gfunc = gfunc
        self.dset = d
        self.vset = v
        self.f = f
    
    #函数返回值
    def _value(self, ph, f):
        raise NotImplementedError
 
class gfunc:
    def __init__(self, kdb, name, byname=''):
        assert type(name) == str
        assert name

        self.kdb = kdb
        assert not self.kdb.getfn(name)
        
        self.name = name
        self.byname = set()     #别名
        
        if byname:
            byname = byname.split('~')
            for name in byname:
                self.addbyname(name)
        self.fn = set()
    
    def addbyname(self, name):
        assert name != self.name
        self.byname.add(name)
    
    def addfn(self, fn):
        assert fn not in self.fn
        self.fn.add(fn)
    
    def getfn(self, ph):
        res = []
        for fn in self.fn:
            if fn.dset[0] == '[':
                dset = fn.dset[1:-1].split(' ')
            else:
                dset = [fn.dset]
            if dset[-1][0] == 'w':
                if len(ph) in [len(dset),len(dset)-1]:
                    for i in range(0, len(dset)-1):
                        if ph[i].be(dset[i])[0] != True:
                            break
                    else:
                        if len(ph) == len(dset)-1:
                            return fn
                        elif ph[-1].s in dset[-1]:
                            return fn
            else:
                if len(ph) == len(dset):
                    for i in range(0,len(dset)):
                        if ph[i].be(dset[i])[0] != True:
                            break
                    else:
                        return fn
        return None
    
    #取值或者判断真假的函数
    def value(self, ph):
        fn = self.getfn(ph)
        if not fn:
            if len(ph) == 1 and len(self.fn) == 1:
                return '%s不是%s'%(ph[0].s, list(self.fn)[0].dset)
            else:
                return '我蒙了'
        return fn._value(ph)

def main():
    print('func')
 
if __name__ == '__main__':
    main()
