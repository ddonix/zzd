#!/usr/bin/python3 -B
from seting import sets

#粘帖集合，目前只有三种。数，汉字数，字符串。无子集
class gsetregu(sets.gset):
    def __init__(self, kdb, name):
        assert name in {'.', '...'}
        sets.gset.__init__(self, kdb, name)

    def spin(self, sp):
        if self.name == '.':
            if not sp.d:
                return (True,{self.name:sp.s})
            else:
                return (False, '')
        else:
            return (True,{self.name:sp.s})
            
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
