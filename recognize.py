import os

from PIL import ImageGrab
import time
from PIL import Image
import numpy as np

from dataload import FireState


def current_equipment():
    gun1 = 'None'
    gun2 = 'None'
    gun1_distance = 11  #武器识别的汉明距离阈值
    gun2_distance = 11
    # print('识别当前配枪')
    # equi_gun_screenshot()
    gun_path = './picture/gun/' #预先截取的demo图片路径
    equi1_path = './picture/equiment/im_1.png' #当前武器图片路径
    equi2_path = './picture/equiment/im_2.png'
    content = os.listdir(gun_path)
    for each in content:
        demopath = gun_path+each
        tmp_dist1 = compare2pic(equi1_path,demopath,10)
        tmp_dist2 = compare2pic(equi2_path, demopath, 10)
        if tmp_dist1 < gun1_distance:
            gun1 = str(each)[:-4]
            gun1_distance = tmp_dist1
        if tmp_dist2 < gun2_distance:
            gun2 = str(each)[:-4]
            gun2_distance = tmp_dist2
    print('1号武器是：'+gun1)
    print('2号武器是：' +gun2)
    return [gun1,gun2]

def current_mirror():
    mirror1 = 'None'
    mirror2 = 'None'
    mirror1_distance = 11  #一号倍镜识别使用的汉明距离阈值
    mirror2_distance = 11  #二号倍镜识别使用的汉明距离阈值
    # print('识别倍镜')
    # equi_part_screenshot()
    mirror_path = './picture/mirrors/' #预先截取的demo图片路径
    mirror1_path = './picture/equiment/mirror_1.png'  #当前倍镜图片路径
    mirror2_path = './picture/equiment/mirror_2.png'
    content = os.listdir(mirror_path)
    for each in content:
        demopath = mirror_path + each
        tmp_dist1 = compare2pic(mirror1_path, demopath, 10)
        tmp_dist2 = compare2pic(mirror2_path, demopath, 10)
        if tmp_dist1 < mirror1_distance:
            mirror1 = str(each)[:-4]
            mirror1_distance = tmp_dist1
        if tmp_dist2 < mirror2_distance:
            mirror2 = str(each)[:-4]
            mirror2_distance = tmp_dist2
    print('1号倍镜是：'+mirror1)
    print('2号倍镜是：' +mirror2)
    return [mirror1,mirror2]

def current_posture():
    '''
    早期的姿势识别函数，原理与武器配件一样使用汉明距离，现在已作废，目前姿势识别采用三点像素取样
    '''
    posture = 'None'
    post_distance = 11
    print('姿势识别')
    posture_screenshot()
    posture_path = './picture/posture/'
    current_posture_path = './picture/equiment/posture.png'
    content = os.listdir(posture_path)
    for each in content:
        demopath = posture_path + each
        tmp_dist = compare2pic(current_posture_path, demopath, 10)
        if tmp_dist < post_distance:
            posture = str(each)[:-4]
            post_distance = tmp_dist
    print('当前姿势：'+posture)
    return

def gun_parts():
    print('识别配件')
    return

def is_bag_open():
    bag_chickpoint_screenshot()
    bag_path = './picture/chickpoint/bag.png'
    cureent_bag_state = './picture/equiment/bag.png'
    tmp_dist = compare2pic(bag_path,cureent_bag_state,5)
    if tmp_dist < 5:
        return True
    else:
        return False

#比对识别图
def get_hash(img):
    hash = ''
    image = Image.open(img)
    image = np.array(image.resize((9, 8), Image.ANTIALIAS).convert('L'), 'f')
    for i in range(8):
        for j in range(8):
            if image[i, j] > image[i, j + 1]:
                hash += '1'
            else:
                hash += '0'
    hash = ''.join(map(lambda x: '%x' % int(hash[x: x + 4], 2), range(0, 64, 4)))  # %x：转换无符号十六进制
    return hash


# get汉明距离
def get_Hamming(hash1, hash2):
    Hamming = 0
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            Hamming += 1
    return Hamming


def compare2pic(equi, demo, threshold):
    equi_hash = get_hash(equi)
    demo_hash = get_hash(demo)
    distance = get_Hamming(equi_hash, demo_hash)
    if distance <= threshold:
        return distance
    return threshold+1

#截图
def make_screenshot(x1, y1, x2,y2):
    bbox = (x1, y1, x2,y2)
    im = ImageGrab.grab(bbox)
    # im.save('./picture/gun/P90.png')
    return im

#当前装备截图
def equi_gun_screenshot():
    im_1 = make_screenshot(1825, 125, 1905, 165)  # 一号枪截图区（此数据适用2K分辨率，其余分辨率或者其余游戏自行调整）
    im_2 = make_screenshot(1825,431,1905,471)  # 二号枪截图区（此数据适用2K分辨率，其余分辨率或者其余游戏自行调整）
    im_1.save('./picture/equiment/im_1.png' )
    im_2.save('./picture/equiment/im_2.png' )

#当前倍镜截图
def equi_part_screenshot():
    im_1 = make_screenshot(2136, 160, 2198, 190)  # 一号倍镜截图区（此数据适用2K分辨率，其余分辨率或者其余游戏自行调整）
    im_2 = make_screenshot(2136, 466, 2198, 496)  # 二号倍镜截图区（此数据适用2K分辨率，其余分辨率或者其余游戏自行调整）
    im_1.save('./picture/equiment/mirror_1.png')
    im_2.save('./picture/equiment/mirror_2.png')

#当前姿势截图
def posture_screenshot():
    im_1 = make_screenshot(946, 1320, 989, 1367)  # 姿势截图区（此数据适用2K分辨率，其余分辨率或者其余游戏自行调整）
    im_1.save('./picture/equiment/posture.png')

#当前背包关键监测点截图
def bag_chickpoint_screenshot():
    img = ImageGrab.grab() #屏幕截图
    bag = img.crop((501,78,573,116)) #提取截屏背包检测点
    im_1 = img.crop((1825, 125, 1905, 165)) #提取截屏武器1
    im_2 = img.crop((1825,431,1905,471)) #提取截屏武器2
    mirror_1 = img.crop((2136, 160, 2198, 190)) #提取截屏倍镜1
    mirror_2 = img.crop((2136, 466, 2198, 496)) #提取截屏倍镜2
    bag.save('./picture/equiment/bag.png')
    im_1.save('./picture/equiment/im_1.png')
    im_2.save('./picture/equiment/im_2.png')
    mirror_1.save('./picture/equiment/mirror_1.png')
    mirror_2.save('./picture/equiment/mirror_2.png')

def get_pixel_gray(pixel):
    gray = 0
    for color in pixel:
        gray += color
    return gray/3

def get_firestate():
    img = ImageGrab.grab()
    firetype = 0
    bullet1 = get_pixel_gray(img.getpixel((1226,1337)))
    bullet2 = get_pixel_gray(img.getpixel((1226,1343)))
    bullet3 = get_pixel_gray(img.getpixel((1223,1358)))
    if bullet1 < 230:
        firetype = 3
    if bullet1 >= 230 and bullet3 >= 230:
        firetype = 0
    if bullet1 >= 230 and bullet2 >= 230 and bullet3 < 230:
        firetype = 2
    if bullet1 >= 230 and bullet2 < 230 and bullet3 < 230:
        firetype = 1

    stand = get_pixel_gray(img.getpixel((964,1311)))
    squat = get_pixel_gray(img.getpixel((969,1338)))
    lie = get_pixel_gray(img.getpixel((981,1347)))
    if stand > squat:
        if stand > lie:
            posture = 0
        else:
            posture = 2
    else:
        if lie > squat:
            posture = 2
        else:
            posture = 1
    state = FireState(posture,firetype)
    return state


if __name__=="__main__":
    # make_screenshot(1825,430,1970,470)
    # equi_gun_screenshot()
    # current_equipment()
    # current_mirror()
    # equi_part_screenshot()
    # current_posture()
    screenshot = ImageGrab.grab()
    pi = screenshot.getpixel((200,90))
    v1 = (pi[0]+pi[1]+pi[2])/3.0
    v2 = 0.299*pi[0]+0.587*pi[1]+0.144*pi[2]
    print(pi)
    print("v1:"+str(v1))
    print("v2:"+str(v2))