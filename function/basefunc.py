#!/usr/bin/python3 -B
from function import func
from seting import categoryset

#求值函数,所有可以通过python eval的表达式都可以
class fnbase(func.fn):
    def __init__(self, gfunc, dset, vset):
        func.fn.__init__(self, gfunc, dset, vset, '')

    #取值或者判断真假的函数
    def _value(self, ph):
        if self.gfunc.name == '如果否则':
            if '(' in ph[0].s:
                return '要递归了'
            else:
                res = eval(ph[0].s)
            if res:
                return ph[1].s
            else:
                return ph[2].s
        elif self.gfunc.name == '大于':
            return int(ph[0].s) > int(ph[1].s)
        elif self.gfunc.name == '大于等于':
            return int(ph[0].s) >= int(ph[1].s)
        elif self.gfunc.name == '小于':
            return int(ph[0].s) < int(ph[1].s)
        elif self.gfunc.name == '小于等于':
            return int(ph[0].s) <= int(ph[1].s)
        elif self.gfunc.name == '不等于':
            return ph[0].s != ph[1].s
        elif self.gfunc.name == '等于':
            return ph[0].s == ph[1].s
        elif self.gfunc.name == '加':
            return int(ph[0].s) + int(ph[1].s)
        elif self.gfunc.name == '减':
            return int(ph[0].s) - int(ph[1].s)
            return ph[0].s == ph[1].s
        elif self.gfunc.name == '乘':
            return int(ph[0].s) * int(ph[1].s)
        elif '除' in self.gfunc.name:
            if self.gfunc.name == '除以':
                x1 = int(ph[0].s)
                x2 = int(ph[1].s)
            else:
                x1 = int(ph[1].s)
                x2 = int(ph[0].s)
            if len(ph) == 3:
                v=ph[2].s
            else:
                v=''
            print(x1,x2,v)
            if x2 == 0:
                return '除数不能为0'
            elif v=='余数':
                return x1%x2
            elif v=='商':
                return int(x1/x2)
            else:
                return x1/x2
        else:
            return '呵呵呵，不是基本函数'

def main():
    print('funccategory')
 
if __name__ == '__main__':
    main()
