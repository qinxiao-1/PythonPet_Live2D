from Config.resources import *
import pyautogui
from pyopengltk import OpenGLFrame
import pygame
from time import sleep
# import live2d.v2 as live2d
import live2d.v3 as live2d
import asyncio

from utils.lipsync import WavHandler
from tts_ws.tts_ws_python3_demo import kdxf_tts, get_wav_duration
from OpenAI.openai_custom import *

class AppOgl(OpenGLFrame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.wavhander = WavHandler()
        self.model = None
        self.respone_message = ''
        self.lipSyncN = 3

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
        if self.wavhander.Update():  # 获取 wav 下一帧片段的响度（Rms），如果没有下一帧片段则为False（音频已播放完毕）
            self.model.AddParameterValue("ParamMouthOpenY", self.wavhander.GetRms() * self.lipSyncN)

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
        self.wavhander.Start(temp_aduio_path)
        pass

    def start_speek_callback(self, group, no):
        print(self.respone_message)
        kdxf_tts(self.respone_message, self.on_tts_finish)

    def chat(self, text):
        pygame.mixer.music.unload()
        def on_finish(str):
            print(str)
            self.model.StartMotion("Speek", 0, live2d.MotionPriority.FORCE, self.start_speek_callback)
            pass
        asyncio.run(start_chat(text, on_finish))
