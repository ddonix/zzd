#!/usr/bin/python3 -B
import element
class fn:
    def __init__(self, gfunc, d, v, f, c=''):
        assert gfunc
        
        self.gfunc = gfunc
        self.dset = d
        self.vset = v
        self.f = f[f.find('=')+1:]
        self.c = set()
        if c:
            c = c.split('~')
            for rec in c:
                rec = rec.split('->')
                self.c.add((rec[0],rec[1]))
            print(self.c)
    
    #函数返回值
    def _v(self, e):
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
        self.fn = None
    
    def addbyname(self, name):
        assert name != self.name
        self.byname.add(name)
    
    def setfn(self, fn):
        assert not self.fn
        self.fn = fn
    
    @classmethod
    def e2list(cls, e):
        res = []
        res.append(e[0:e.find('(')])
        e=e[e.find('(')+1:-1]
        ss = e
        while ss:
            r = cls._e2list(ss)
            res.append(r[0])
            ss = r[1]
        return res

    @classmethod
    def _e2list(cls, ss):
        assert ss
        if ',' not in ss:
            return (ss,'')
        else:
            i = ss.find(',')
            if '(' not in ss[0:i]:
                return (ss[0:i],ss[i+1:])
            else:
                c = ss[0:i].count('(')
                j = 0
                for j in range(0,len(ss)):
                    if ss[j] == ')':
                        c -= 1
                        if not c:
                            break
                return (ss[0:j+1],ss[j+2:])
    
    def getfne(self, e):
        name = e[0:e.find('(')]
        if name == self.name or name == 'f':
            return self.fn
        else:
            print(self)
            print(self.kdb)
            gfn = self.kdb.getfn(name)
            return gfn.fn

    def getfn(self, ph):
        if not self.fn:
            return None
        fn = self.fn
        if fn.dset[0] == '[':
            dset = fn.dset[1:-1].split(' ')
        else:
            dset = [fn.dset]
        if dset[-1][0] == 'w':
            if len(ph) in [len(dset),len(dset)-1]:
                for i in range(0, len(dset)-1):
                    if ph[i].be(dset[i])[0] != True:
                        return None
                else:
                    if len(ph) == len(dset)-1:
                        return fn
                    elif ph[-1].s in dset[-1]:
                        return fn
        else:
            if len(ph) == len(dset):
                for i in range(0,len(dset)):
                    if ph[i].be(dset[i])[0] != True:
                        return None
                else:
                    return fn
    
    #取值或者判断真假的函数
    def value(self, ph):
        fn = self.getfn(ph)
        if not fn:
            if len(ph) == 1: 
                return '%s不是%s'%(ph[0].s, self.fn.dset)
            else:
                return '我蒙了'
        e = '%s(%s'%(self.name,ph[0].s)
        for p in ph[1:]:
            e += ',%s'%p.s
        e +=')'
        return self.v(e)

    def v(self, e):
        print('e:',e)
        if '(' not in e:
            ph = self.kdb.getph(e)
            if e == 'True':
                return True
            elif e == 'False':
                return False
            elif ph and ph.be('数')[0] == True:
                return int(e)
            else:
                return e
        else:
            li = gfunc.e2list(e)
            ee=e
            ee = '%s'%li[0]
            ee += '(%s'%(self.v(li[1]) if '(' in li[1] else li[1])
            for s in li[2:]:
                ee += ',%s'%(self.v(s) if '(' in s else s)
            ee += ')'
            fn = self.getfne(ee)
            print('ee:',ee)
            return fn._v(ee)

def main():
    print('func')
 
if __name__ == '__main__':
    main()
