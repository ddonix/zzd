#!/usr/bin/python3 -B

class cmd:
    def __init__(self, zhd):
        self.zhd = zhd
    
    def input(self, adapter):
        assert 'zzd命令' in adapter
        zhd = self.zhd
        if '命令参数' in adapter:
            arg = adapter['命令参数']
        else:
            arg = ''
        exe = zhd.KDB.keyword[adapter['zzd命令']][1]
        if exe:
            zhd.say('还在开发中')
            return
        if zhd.FSM['verify'] == False:
            if 'zzd认证命令' in adapter:
                zhd.desire['verify'][1] = True
                zhd.desire['verify'][2] = arg
            else:
                zhd.say('请先认证身份')
            return
        if 'zzd认证命令' in adapter:
            zhd.say('请已经认证过身份了.同时服务多人功能正在开发中')
        elif 'zzd播放命令' in adapter:
            out = zhd.player.play(arg)
        elif 'zzd换曲命令' in adapter:
            out = zhd.player.next()
        elif 'zzd暂停命令' in adapter:
            out = zhd.player.pause()
        elif 'zzd继续命令' in  adapter:
            out = zhd.player.con()
        elif 'zzd停止命令' in adapter:
            out = zhd.player.stop(True)
        elif 'zzd再见命令' in adapter:
            zhd.add_desire('goodbye', '%s！'%adapter['zzd再见命令'])
        elif 'zzd保存命令' in adapter:
            zhd._command_save()
        elif 'zzd学习命令' in adapter or 'zzd进入命令' in adapter:
            if zhd.FSM['train'] == False:
                zhd.say('好的，已进入学习模式！')
                zhd.FSM['train'] = True
            else:
                zhd.say('您已经是学习模式了')
        elif 'zzd退出命令' in adapter:
            mode = adapter['zzd学习命令'] if 'zzd学习命令' in adapter else adapter['zzd模式定语_学习']
            if zhd.FSM['train'] == True:
                zhd.say('好的，已退出%s模式'%mode)
                zhd.FSM['train'] = False
            else:
                zhd.say('您并没有在%s模式'%mode)
        else:
            zhd.say('不识别的内置命令')

    def _command_save(self):
        zhd = self.zhd
        infonum = zhd.KDB.getinfonum()
        if infonum == 0:
            zhd.say('没有信息要写入数据库')
            return
        zhd.say('请输入管理员口令')
        password = zhd.ask(['认证参数句','认证参数'])
        if not password:
            zhd.say('您没有输入口令，写入取消。')
            return
        password = password['认证参数']
        if password != zhd.managerid:
            zhd.say('口令错误，写入取消。')
            return
            
        res = zhd.KDB.save_infomation(zhd.friend.name)
        if res[0] == False:
            zhd.say(res[1])
        else:
            zhd.say('成功写入%d条信息'%res[1])
            if res[1] < infonum:
                zhd.say('%d条信息写入失败'%res[2])
    
def main():
    print('command')

if __name__ == '__main__':
    main()
