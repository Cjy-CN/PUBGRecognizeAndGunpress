import multiprocessing
from multiprocessing import Process
from threading import Thread
from pynput import mouse,keyboard
from win32gui import GetWindowText, GetForegroundWindow
from gun_press import *


def start_mouse_listen(dict):

    def on_button_click(x, y, button, pressed):
        nonlocal dict
        if button == button.left:
            if pressed and '绝地求生' in GetWindowText(GetForegroundWindow()):
                dict['fire_signal'] = True
            else:
                dict['fire_signal'] = False
        else:
            pass
        return True

    with mouse.Listener(on_click=on_button_click) as listener:
        listener.join()


def start_key_listen(dict):  # 键盘监听,非阻塞
    def on_key_press(key):
        nonlocal dict
        if '绝地求生' in GetWindowText(GetForegroundWindow()):
            if key == keyboard.Key.tab:
                if dict['key_pressed']:
                    return True
                dict['key_pressed'] = True
                dict['bag_signal'] = True
            elif key == keyboard.KeyCode.from_char('1'):
                dict['switch'] = 0
            elif key == keyboard.KeyCode.from_char('2'):
                dict['switch'] = 1
            if dict['fire_signal']:
                # 开火过程中才对卧(z)，蹲（c/ctrl），切换开火模式(b)的按键进行检测，检测到则更新当前开火状态
                if key == keyboard.KeyCode.from_char(
                        'z') or key == keyboard.Key.ctrl or key == keyboard.KeyCode.from_char(
                    'b') or key == keyboard.KeyCode.from_char('c'):
                    firestate_struct = get_firestate()
                    dict['posture'] = firestate_struct.posture
                    dict['firemode'] = firestate_struct.firetype

    def on_key_release(key):
        nonlocal dict
        dict['key_pressed'] = False

    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()


def start_listen(dict):
    t1 = Thread(target=start_mouse_listen,args=(dict,))
    t2 = Thread(target=start_key_listen,args=(dict,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
1
if __name__=='__main__':
    multiprocessing.freeze_support()
    mgr = multiprocessing.Manager()
    dict = mgr.dict()
    dict['key_pressed'] = False
    dict['fire_signal'] = False
    dict['firestate_inspect'] = False
    dict['bag_signal'] = False
    dict['switch'] = 0
    dict['posture'] = 0
    dict['firemode'] = 3
    p_fire = Process(target=fire,args=(dict,))
    p_listen = Process(target=start_listen,args=(dict,))
    p_listen.start()
    p_fire.start()
    p_listen.join()
    p_fire.join()