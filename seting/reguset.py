#!/usr/bin/python3 -B
from seting import sets

#粘帖集合，目前只有三种。数，汉字数，字符串。无子集
class gsetregu(sets.gset):
    def __init__(self, kdb, name):
        assert name in {'.', '...'}
        sets.gset.__init__(self, kdb, name)
        self.plot = ''

    def phin(self, ph):
        return (True,{self.name:sp.s})

    def setplot(self, p):
        self.plot = p
    
    def _sein(self, phs):
        if self.name == '.':
            return (phs[0].s, phs[1:], {self.name:phs[0].s})
        else:
            sps = ''
            while phs:
                if phs[0].be('分隔词')[0] == True:
                    break
                if self.plot:
                    if phs[0].be(self.plot)[0] == True:
                        break
                sps += phs[0].s
                phs = phs[1:]
            return (sps, phs, {self.name:sps})
            
    def weight(self):               #返回集合的元素个数，无穷集合返回-1.
        return -1
    
    def affirm1(self, sp):           #sp属于self.不支持断言.
        return (False, 'stickset不支持断言元素')
    
    def affirm2(self, gs):           #gs包含于self.没有子集
        return (False, 'stickset不支持断言子集')
    
def main():
    print('stickset')

if __name__ == '__main__':
    main()
