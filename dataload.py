import codecs
import json

class FireState:
    def __init__(self, posture, firetype,hasbullet):
        self.posture = posture #站0，蹲1，卧2
        self.firetype = firetype #全自动0，单发1，连发2，检测不到3（没枪）
        self.hasbullet = hasbullet

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
    pass

