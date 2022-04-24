# PUBGRecognizeAndGunpress

# 注意
- 本项目的配件识别是基于截取屏幕固定位置识别的，受限于开发条件，只适配于2560*1440的屏幕
- 请先安装好LGS_9.02.65_x64_Logitech.exe。因为压枪是基于调用罗技鼠标驱动实现的（即使你的鼠标不是罗技的也没有关系）
- 最好使用简体中文界面，否则有少数枪械无法识别
- 没做图形界面（感觉也不需要）

# 如何打包为可执行程序.exe
1. 执行pyinstaller monitor.py -p dataload.py -p ghub.py -p gun_press.py -p recognize.py
2. 把“ghub_device.dll”，“枪械数据”文件夹,“picture”文件夹放到上一步生成的dict目录中

# 如何调试代码
执行monitor.py的if __name__=='__main__'
