#!/usr/bin/python3 -B

class nature:
    def __init__(self, zhd):
        self.zhd = zhd
        self.FSM = {'wait':True}
    
    def input(self, adapter):
        if '称呼' in adapter and adapter['称呼'] == adapter['聊天语句']:
            self.zhd.say('我在')
        elif '问候' in adapter:
            self.zhd.say('你好')
        else:
            self.zhd.say('你说啥')

def main():
    print('hmnature')

if __name__ == '__main__':
    main()
