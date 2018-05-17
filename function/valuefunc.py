#!/usr/bin/python3 -B
from function import func
from seting import categoryset

#求值函数,所有可以通过python eval的表达式都可以
class gfuncvalue(func.gfunc):
    def __init__(self, kdb, name, desc):
        func.gfunc.__init__(self, kdb, name, desc)

    #取值或者判断真假的函数
    def _value(self, se, fn):
        assert fn[2]
        if fn[0] == '数':
            if fn[2].find('eval(x)') != -1:
                e = fn[2].replace('eval(x)','(%s)'%se.s)
            else:
                e = fn[2]
            return eval(e)
        else:
            return None
    
    def judge(self, se, desp):
        return None

def parsefunc(kdb, fn):
    assert fn[1] == '求值'
    func = gfuncvalue(kdb, fn[0], fn[2])
    return func

def main():
    print('funccategory')
    
if __name__ == '__main__':
    main()
