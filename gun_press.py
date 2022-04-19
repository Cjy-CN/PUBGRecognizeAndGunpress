from multiprocessing import shared_memory
from ghub import *
import time
from dataload import Gun
from recognize import *

def fire():
    fire_signal = shared_memory.ShareableList(name='fire_signal')
    switch = shared_memory.ShareableList( name='switch')
    fire_state = shared_memory.ShareableList(name='fire_state')
    while True:
        if fire_signal[0] :
            start_time = round(time.perf_counter(), 3) * 1000
            firestate_struct = get_firestate()
            fire_state[0] = firestate_struct.posture
            fire_state[1] = firestate_struct.firetype
            #在这里加一个没子弹检测
            if not firestate_struct.hasbullet:
                continue
            i = 0
            gun = Gun()
            gun1 = shared_memory.ShareableList(name='gun1')
            gun2 = shared_memory.ShareableList( name='gun2')
            if switch[0] == 0:
                gun = Gun(gun1[0],gun1[1],gun1[2],gun1[3],gun1[4])
            else:
                gun = Gun(gun2[0], gun2[1], gun2[2], gun2[3], gun2[4])
            if gun.para_time.__len__() < 1:
                continue
            print('开始为'+gun.name+'压枪')
            if fire_state[1] == 0: #全自动模式压枪
                print('全自动模式压枪')
                while True:
                    # if fire_state[1] == 3:
                    #     break #没枪不压
                    posture_ratio = gun.posture_states[fire_state[0]]
                    down = gun.para_range[i] * gun.k * posture_ratio * 0.057
                    # print("下压幅度:"+str(down))
                    mouse_xy(0, down)
                    elapsed = (round(time.perf_counter(), 3) * 1000 - start_time)
                    print(elapsed)
                    if elapsed > gun.para_time[i]:
                        i += 1
                    if i >= gun.para_time.__len__() or not fire_signal[0]:
                        break
                    time.sleep(0.02)
            elif fire_state[1] == 1: #单点模式压枪
                print('单点模式压枪')
                # 哪位老哥来完善一下，成了就能把连狙变成全自动了
        else:
            pass