from multiprocessing import shared_memory
from ghub import *
import time
from dataload import Gun
from recognize import *

def fire():
    Guns = []
    fire_signal = shared_memory.ShareableList(name='fire_signal')
    switch = shared_memory.ShareableList( name='switch')
    fire_state = shared_memory.ShareableList(name='fire_state')
    bag_signal = shared_memory.ShareableList(name='bag_signal')
    while True:
        if bag_signal[0]:
            if is_bag_open():
                Guns = recognize_equiment()
            bag_signal[0] = False
        if fire_signal[0]:
            if not bullet_check():
                continue
            start_time = round(time.perf_counter(), 3) * 1000
            firestate_struct = get_firestate()
            fire_state[0] = firestate_struct.posture
            fire_state[1] = firestate_struct.firetype
            if len(Guns) > switch[0]:
                gun = Guns[switch[0]]
                if gun.name == 'None':
                    continue
                i = 0
                if gun.single == False:  #不是单发的枪
                    while True:
                        posture_ratio = gun.posture_states[fire_state[0]]
                        down = gun.para_range[i] * posture_ratio * gun.k * 0.874
                        i += 1
                        if i == gun.maxBullets or not fire_signal[0]:
                            break
                        mouse_xy(0, down)
                        elapsed = (round(time.perf_counter(), 3) * 1000 - start_time)
                        sleeptime = gun.interval - elapsed
                        time.sleep(sleeptime/1000)
                        start_time = round(time.perf_counter(), 3) * 1000
                else:
                    pass