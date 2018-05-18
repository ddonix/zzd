#!/usr/bin/python3 -B
from function import func
from seting import categoryset

#求值函数,所有可以通过python eval的表达式都可以
class gfuncvalue(func.gfunc):
    def __init__(self, kdb, name, desc, byname):
        func.gfunc.__init__(self, kdb, name, desc, byname)

    #取值或者判断真假的函数
    def _value(self, ph, fn):
        assert fn[2]
        print(ph, fn)
        e = fn[2].replace('如果','if')
        e = e.replace('否则','else')
        if len(ph) == 1:
            e = e.replace('x','(%s)'%ph[0].s)
        else:
            for i in range(0,len(ph)-1):
                e = e.replace('x%d'%(i+1),'(%s)'%ph[i].s)
            if 'v' in e:
                e = e.replace('v','("%s")'%(ph[-1].s if ph[-1] else 'default'))
        return eval(e)
    
    def judge(self, ph, desp):
        return None

def parsefunc(kdb, fn):
    assert fn[1] == '求值'
    func = gfuncvalue(kdb, fn[0], fn[2], fn[3])
    return func

def main():
    print('funccategory')
    
if __name__ == '__main__':
    main()
