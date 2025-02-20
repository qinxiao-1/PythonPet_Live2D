from resources import *
import tkinter

import pyautogui
from pyopengltk import OpenGLFrame

from time import sleep
# import live2d.v2 as live2d
import live2d.v3 as live2d

import winsound
import pygame
from utils.lipsync import WavHandler
wavhander = WavHandler()
lipSyncN = 3

def onStartCallback(group: str, no: int):
    print(f"touched and motion [{group}_{no}] is started")

# 动作播放结束后会调用该函数
def onFinishCallback():
    print("motion finished")

def start_callback(group, no):
    wav_path = r".\Resources\Audio\audio1.wav"
    print("start")
    # 播放音频
    # pygame.mixer.music.load(wav_path)
    # pygame.mixer.music.play()
    # 播放 .wav 文件
    # winsound.PlaySound(r".\Resources\Audio\audio1.wav", winsound.SND_FILENAME)
    # 处理口型同步
    # wavhander.Start(wav_path)

class AppOgl(OpenGLFrame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.model = None


    def initgl(self):
        """Initalize gl states when the frame is created"""
        if self.model:
            del self.model
        live2d.dispose()

        live2d.init()
        live2d.glewInit()
        
        pygame.mixer.init()
        # Touch(0, 0, onStartCallback, onFinishCallback)

        self.model = live2d.LAppModel()
        if live2d.LIVE2D_VERSION == 2:
            self.model.LoadModelJson(kasumi2_v2)
        else:
            self.model.LoadModelJson(Hiyori_v3)
            # self.model.LoadModelJson(os.path.join(resources.RESOURCES_DIRECTORY, "\Resources\V3\Hiyori\Hiyori.model3.json"))
        self.model.Resize(self.width, self.height)
        # self.model.Touch(0, 0, onStartCallback, onFinishCallback)
        # 强制开始动作
        # self.model.StartMotion("TapBody", 0, live2d.MotionPriority.FORCE, onStartCallback, onFinishCallback)
        self.model.StartMotion("Idle", 5, live2d.MotionPriority.FORCE, onStartCallback, onFinishCallback)
        # 强制开始说话
        # self.model.StartMotion("Speek", 0, live2d.MotionPriority.FORCE, start_callback)


    def redraw(self):
        """Render a single frame"""
        live2d.clearBuffer()

        screen_x, screen_y = pyautogui.position()
        x = screen_x - self.winfo_rootx()
        y = screen_y - self.winfo_rooty()

        self.model.Update()

        # 在 Update 之后，Draw 之前调用
        if wavhander.Update():  # 获取 wav 下一帧片段的响度（Rms），如果没有下一帧片段则为False（音频已播放完毕）
            self.model.AddParameterValue("ParamMouthOpenY", wavhander.GetRms() * lipSyncN)

        self.model.Drag(x, y)
        self.model.Draw()

        # 控制帧率
        sleep(1 / 60)

if __name__ == '__main__':
    root = tkinter.Tk()
    root.overrideredirect(True)
    root.attributes('-transparent', 'black')
    window_width = 400
    window_height = 500
    root.geometry(f"{window_width}x{window_height}")
    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # 计算窗口的右下角坐标
    x_position = screen_width - window_width
    y_position = screen_height - window_height
    # 设置窗口位置
    root.geometry(f"+{x_position}+{y_position}")
    # 强制设置窗口在最顶层
    root.attributes("-topmost", True)

    app = AppOgl(root, width=window_width, height=window_height)
    root.bind("<Button-1>", lambda _: app.model.StartRandomMotion())
    app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    app.animate = 1
    app.mainloop()

    live2d.dispose()
    pygame.mixer.quit()