#!/usr/bin/python3 -B
import time

#output函数运行在root主进程
#input函数运行在zhd线程
#其他函数运行在xhh线程.
class human():
    def __init__(self, name):
        self.name = name
        self.working = True
        self.root = True
    
    @classmethod
    def init(cls):
        print('human init')

    #运行在zhd线程
    def input(self, sour, waa):
        for bye in ('再见', '拜拜', '晚安', '午安'):
            if bye in waa:
                self.working = False
        #这里体现人不理会机器的反应
        pass
    
    #运行在root主进程
    def output(self, dest, waa):
        dest.input(self, waa)
    
    def live(self):
        while self.working and self.root:
            time.sleep(1)

def main():
    print('zzd_human')
    human.init()

if __name__ == '__main__':
    main()
