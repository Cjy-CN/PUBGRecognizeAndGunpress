from ghub import *
import time
from recognize import *

def fire(dict):
    Guns = []
    while True:
        if dict['bag_signal']:
            if is_bag_open():
                Guns = recognize_equiment()
            dict['bag_signal'] = False
        if dict['fire_signal']:
            if not bullet_check():
                continue
            start_time = round(time.perf_counter(), 3) * 1000
            firestate_struct = get_firestate()
            dict['posture'] = firestate_struct.posture
            dict['firemode'] = firestate_struct.firetype
            if len(Guns) > dict['switch']:
                gun = Guns[dict['switch']]
                if gun.name == 'None':
                    continue
                i = 0
                if gun.single == False:  #不是单发的枪
                    while True:
                        posture_ratio = gun.posture_states[dict['posture']]
                        down = gun.para_range[i] * posture_ratio * gun.k
                        i += 1
                        if i == gun.maxBullets or not dict['fire_signal']:
                            break
                        mouse_xy(0, down)
                        elapsed = (round(time.perf_counter(), 3) * 1000 - start_time)
                        sleeptime = gun.interval - elapsed
                        time.sleep(sleeptime/1000)
                        start_time = round(time.perf_counter(), 3) * 1000
                else: #连狙压枪
                    while True:
                        posture_ratio = gun.posture_states[dict['posture']]
                        down = gun.para_range[i] * posture_ratio * gun.k
                        i += 1
                        if i == gun.maxBullets or not dict['fire_signal']:
                            break
                        mouse_xy(0, down)
                        elapsed = (round(time.perf_counter(), 3) * 1000 - start_time)
                        sleeptime = gun.interval - elapsed
                        time.sleep(sleeptime / 1000)
                        click_key('/')
                        start_time = round(time.perf_counter(), 3) * 1000

