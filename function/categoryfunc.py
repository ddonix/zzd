#!/usr/bin/python3 -B
from function import func

#分类集合，枚举集合的划分。例如:人划分为男人和女人
class gfunccategory(func.gfunc):
    def __init__(self, kdb, name, desc):
        func.gfunc.__init__(self, kdb, name, desc)

    #取值或者判断真假的函数
    def value_a(self, sp):
        return None
    
    def affirm_a(self, sp, desp):
        return None
    
    def judge_a(self, sp, desp):
        return None
    
    def value_A(self, gs):
        return None

def parsefunc(kdb, fn):
    return None

def main():
    print('funccategory')
    
if __name__ == '__main__':
    main()
