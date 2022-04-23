import multiprocessing
from multiprocessing import Process
from multiprocessing import shared_memory
from threading import Thread
from pynput import mouse,keyboard
from dataload import Gun
from win32gui import GetWindowText, GetForegroundWindow
from recognize import *
from gun_press import *

def start_mouse_listen():
    with mouse.Listener(on_click=on_button_click) as listener:
        listener.join()

def on_button_click(x,y,button,pressed):
    fire_signal = shared_memory.ShareableList(name='fire_signal')
    if button == button.left:
        if pressed and '绝地求生' in GetWindowText(GetForegroundWindow()):
            fire_signal[0] = True
        else:
            fire_signal[0] = False
    else:
        pass
    return True

def start_key_listen(): #键盘监听,非阻塞
    with keyboard.Listener(on_press=on_key_press,on_release=on_key_release) as listener:
        listener.join()

def on_key_press(key):
    switch = shared_memory.ShareableList( name='switch')
    key_pressed = shared_memory.ShareableList( name='key_pressed')
    fire_state = shared_memory.ShareableList(name='fire_state')
    fire_signal = shared_memory.ShareableList( name='fire_signal')
    bag_signal = shared_memory.ShareableList( name='bag_signal')
    if '绝地求生' in GetWindowText(GetForegroundWindow()):
        if key == keyboard.Key.tab:
            if key_pressed[0]:
                return True
            key_pressed[0] = True
            bag_signal[0] = True
        elif key ==  keyboard.KeyCode.from_char('1'):
            switch[0] = 0
        elif key == keyboard.KeyCode.from_char('2'):
            switch[0] = 1
        if fire_signal[0]:
            # 开火过程中才对卧(z)，蹲（c/ctrl），切换开火模式(b)的按键进行检测，检测到则更新当前开火状态
            if key == keyboard.KeyCode.from_char('z') or key == keyboard.Key.ctrl or key == keyboard.KeyCode.from_char('b') or key == keyboard.KeyCode.from_char('c'):
                firestate_struct = get_firestate()
                fire_state[0] = firestate_struct.posture
                fire_state[1] = firestate_struct.firetype

def on_key_release(key):
    key_pressed = shared_memory.ShareableList(name='key_pressed')
    key_pressed[0] = False

def start_listen():
    t1 = Thread(target=start_mouse_listen)
    t2 = Thread(target=start_key_listen)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__=='__main__':
    multiprocessing.freeze_support()
    print('start')
    # 定义了一堆多进程的“全局变量” py3.8以上支持
    try:
        a1 = shared_memory.ShareableList([False], name='key_pressed')
        a2 = shared_memory.ShareableList([False], name='fire_signal')
        a3 = shared_memory.ShareableList([False], name='firestate_inspect')
        a4 = shared_memory.ShareableList([0], name='switch')
        a5 = shared_memory.ShareableList([0,3], name='fire_state') #第一个值是人物姿势，第二个值是开火模式
        a6 = shared_memory.ShareableList([False], name='bag_signal')
    except:
        pass
    p_fire = Process(target=fire)
    p_listen = Process(target=start_listen)
    p_listen.start()
    p_fire.start()
    p_listen.join()
    p_fire.join()