from resources import *
import tkinter

import pyautogui
from pyopengltk import OpenGLFrame

from time import sleep
# import live2d.v2 as live2d
import live2d.v3 as live2d
from threading import Timer

import pygame
from utils.lipsync import WavHandler
from OpenAI.opai_test import request_openai
from tts_ws_python3_demo.tts_ws_python3_demo import kdxf_tts, get_wav_duration

wavhander = WavHandler()
lipSyncN = 3

class AppOgl(OpenGLFrame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.model = None
        self.respone_message = ''

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
        # self.model.StartMotion("Idle", 5, live2d.MotionPriority.FORCE, onStartCallback, onFinishCallback)
        # 强制开始说话
        # self.model.StartMotion("Speek", 0, live2d.MotionPriority.FORCE, start_speak_callback)

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

    def onStartCallback(self, group: str, no: int):
        print(f"touched and motion [{group}_{no}] is started")

    # 动作播放结束后会调用该函数
    def onFinishCallback(self):
        print("motion finished")

    def on_tts_finish(self):
        # 播放音频
        pygame.mixer.music.load(temp_aduio_path)
        pygame.mixer.music.play()
        wav_length = get_wav_duration(temp_aduio_path)
        # 处理口型同步
        wavhander.Start(temp_aduio_path)
        pass

    def start_speek_callback(self, group, no):
        print(self.respone_message)
        kdxf_tts(self.respone_message, self.on_tts_finish)

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

    # 
    root.title("Tkinter 输入框示例")
    entry = tkinter.Entry(root, width=40)
    entry.pack(pady=10)

    def on_button_click():
        user_input = entry.get()
        pygame.mixer.music.unload()
        app.respone_message = request_openai(user_input)
        app.model.StartMotion("Speek", 0, live2d.MotionPriority.FORCE, app.start_speek_callback)

    # 创建确定按钮
    button = tkinter.Button(root, text="确定", command=on_button_click)
    button.pack(pady=5)

    #  root.bind("<Button-1>", lambda _: app.model.StartRandomMotion())
    app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    app.animate = 1


    app.mainloop()

    live2d.dispose()
    pygame.mixer.quit()