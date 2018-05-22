#!/usr/bin/python3 -B
from function import func
from seting import categoryset

#求值函数,所有可以通过python eval的表达式都可以
class fnbase(func.fn):
    def __init__(self, gfunc, dset, vset):
        func.fn.__init__(self, gfunc, dset, vset, '')

    #取值或者判断真假的函数
    def _v(self, e):
        li = func.gfunc.e2list(e)
        if self.gfunc.name == '如果否则':
            if li[1]:
                return li[2]
            else:
                return li[3]
        elif self.gfunc.name == '大于':
            return int(li[1]) > int(li[2])
        elif self.gfunc.name == '大于等于':
            return int(li[1]) >= int(li[2])
        elif self.gfunc.name == '小于':
            return int(li[1]) < int(li[2])
        elif self.gfunc.name == '小于等于':
            return int(li[1]) <= int(li[2])
        elif self.gfunc.name == '不等于':
            return li[1] != li[2]
        elif self.gfunc.name == '等于':
            return li[1] == li[2]
        elif self.gfunc.name == '加':
            return int(li[1]) + int(li[2])
        elif self.gfunc.name == '减':
            return int(li[1]) - int(li[2])
        elif self.gfunc.name == '乘':
            return int(li[1]) * int(li[2])
        elif '除' in self.gfunc.name:
            if self.gfunc.name == '除以':
                x1 = int(li[1])
                x2 = int(li[2])
            else:
                x1 = int(li[2])
                x2 = int(li[1])
            if len(li) == 4:
                v=li[3]
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
    print('funcbase')
 
if __name__ == '__main__':
    main()
