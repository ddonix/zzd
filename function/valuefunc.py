#!/usr/bin/python3 -B
from function import func
from seting import categoryset

#求值函数,所有可以通过python eval的表达式都可以
class fnvalue(func.fn):
    def __init__(self, gfunc, dset, vset, f):
        func.fn.__init__(self, gfunc, dset, vset, f)

    #取值或者判断真假的函数
    def _value(self, ph):
        e = self.f.replace('如果','if')
        e = e.replace('否则','else')
        if 'f' not in self.f:
            if len(ph) == 1:
                e = e.replace('x','(%s)'%ph[0].s)
            else:
                for i in range(0,len(ph)-1):
                    e = e.replace('x%d'%(i+1),'(%s)'%ph[i].s)
                if 'v' in e:
                    e = e.replace('v','("%s")'%(ph[-1].s if ph[-1] else 'default'))
            return eval(e)
        else:
            print(self.f)
            return '呵呵呵，递归了哦'
    
def main():
    print('funccategory')
 
if __name__ == '__main__':
    main()
