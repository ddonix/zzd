#!/usr/bin/python3 -B
from seting import sets

#粘帖集合，目前只有三种。数，汉字数，字符串。无子集
class gsetstick(sets.gset):
    def __init__(self, kdb, name):
        assert name in {'数', '汉语数', '字符串'}
        sets.gset.__init__(self, kdb, name)

    def phin(self, ph):
        znumber =  '0123456789'
        cnumber =  '零一二三四五六七八九十百千万亿'
        zstr1 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        zstr2 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if self.name == '数':
            f = znumber
        elif self.name == '汉语数':
            f = cnumber
        else:
            if ph.s[0] not in zstr2:
                return (False, '')
            f = zstr1
        for s in ph.s:
            if s not in f:
                return (False, '')
        return (True,{self.name:ph.s})
    
    def _sein(self, phs):
        if phs and self.phin(phs[0])[0] == True:
            return (phs[0].s, phs[1:], {self.name:phs[0].s})
        return None
    
    def weight(self):               #返回集合的元素个数，无穷集合返回-1.
        return -1
    
    def affirm1(self, ph):           #ph属于self.不支持断言.
        return (False, 'stickset不支持断言元素')
    
    def affirm2(self, gs):           #gs包含于self.没有子集
        return (False, 'stickset不支持断言子集')
    
    def affirm3(self, sp):           #sp属于self.不支持断言.
        return (False, 'stickset不支持断言元素')
    
def main():
    print('stickset')

if __name__ == '__main__':
    main()
