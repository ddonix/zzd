#!/usr/bin/python3 -B
from seting import sets

#粘帖集合，目前只有三种。数，汉字数，字符串。无子集
class gsetregu(sets.gset):
    def __init__(self, kdb, name):
        assert name in {'.', '...'}
        sets.gset.__init__(self, kdb, name)
        self.plot = ''

    def phin(self, ph):
        return (True,{self.name:ph.s})

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
                        self.plot = ''
                        break
                sps += phs[0].s
                phs = phs[1:]
            return (sps, phs, {self.name:sps})
            
    def weight(self):               #返回集合的元素个数，无穷集合返回-1.
        return -1
    
def main():
    print('stickset')

if __name__ == '__main__':
    main()
