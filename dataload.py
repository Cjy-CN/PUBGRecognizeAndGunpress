import codecs
import re
import json

class Gun:

    def __init__(self,name='None',mirror='',muzzle='',grip='',butt=''):
        '''

        :param name: 武器名称
        :param mirror: 倍镜
        :param muzzle: 枪口
        :param grip: 握把
        :param butt: 枪托
        '''
        self.name = name
        self.para_time = [] #段落时间
        self.para_range = [] #每段下压幅度
        self.posture_states = [1,]
        self.parts = [mirror,muzzle,grip,butt] #配件列表
        self.k = 1.0 #配件压枪系数,最后结果由各部分配件累乘得到
        self.interval = 0 #每发射击间隔
        if name != "None":
            try:
                with codecs.open("./枪械数据/"+name+".txt",'r','gb2312') as f:
                    contents = f.readlines()
                    pattern = re.compile(r'：\d+')
                    s = pattern.search(contents[1]).group(0)[1:] #从配置文件第二行获取子弹间隔时间
                    self.interval = int(s)
                    str_time = contents[2][5:] #从配置文件第三行，第六个字符开始获取段落时间的字符串
                    str_range = contents[3][5:] #从配置文件第四行，第六个字符开始获取压枪幅度的字符串
                    self.para_time = [int(x) for x in str_time.split('-')]
                    self.para_range = [int(x) for x in str_range.split('-')]
                    pattern = re.compile(r'=\d+(\.\d+)?')
                    for line in contents[5:]:
                        for part in self.parts:
                            if part != '' and part != 'None':
                                if line.find(part) >= 0:
                                    s = pattern.search(line).group(0)[1:]
                                    self.k *= float(s)
                        if line.find('蹲姿') >= 0:
                            s = pattern.search(line).group(0)[1:]
                            self.posture_states.append(float(s))
                        if line.find('卧姿') >= 0:
                            s = pattern.search(line).group(0)[1:]
                            self.posture_states.append(float(s))

            except Exception as e:
                print(type(e),'::',e)
        else:
            pass

class FireState:
    def __init__(self, posture, firetype,hasbullet):
        self.posture = posture #站0，蹲1，卧2
        self.firetype = firetype #全自动0，单发1，连发2，检测不到3（没枪）
        self.hasbullet = hasbullet

class GunTest:
    def __init__(self,name='None',mirror='',muzzle='',grip='',butt=''):
        '''
        :param name: 武器名称
        :param mirror: 倍镜
        :param muzzle: 枪口
        :param grip: 握把
        :param butt: 枪托
        '''
        self.name = name
        self.para_range = []  # 每段下压幅度
        self.posture_states = [1, ]
        self.parts = [mirror, muzzle, grip, butt]  # 配件列表
        self.k = 1.0  # 配件压枪系数,最后结果由各部分配件累乘得到
        self.interval = 0  # 每发射击间隔
        self.maxBullets = 0 #子弹最大数量
        self.single = False #是否单发
        if name != "None" and name != '':
            try:
                with codecs.open("./枪械数据/game.json") as f:
                    game_data = json.load(f)
                    gun_data = game_data['list'][name]
                    self.name = gun_data['name']
                    self.maxBullets = gun_data['maxBullets']
                    self.single = gun_data['single']
                    self.interval = gun_data['speed']
                    self.para_range = gun_data['ballistic']
                    self.posture_states.append(gun_data['posture']['squat'])
                    self.posture_states.append(gun_data['posture']['down'])
                    if mirror!= 'None' and mirror != '':
                        self.k *= gun_data['mirror'][mirror]
                    if muzzle != 'None' and muzzle != '':
                        self.k *= gun_data['muzzle'][muzzle]
                    if grip != 'None' and grip != '':
                        self.k *= gun_data['grip'][grip]
                    if butt != 'None' and muzzle != '':
                        self.k *= gun_data['butt'][butt]
            except Exception as e:
                print(type(e), '::', e)
        else:
            pass

if __name__ == '__main__':
    GunTest('ace32',muzzle='1')

