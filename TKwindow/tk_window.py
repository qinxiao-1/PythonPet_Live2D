import tkinter
import live2d.v3 as live2d
import pygame
import asyncio

from Live2DAppOgl.Live2DAppOgl import AppOgl
from OpenAI.openai_custom import *

class tkwindow():
    def __init__(self):
        self.root = tkinter.Tk()
        self.window_config()
        pass

    def window_config(self):
        # self.root.overrideredirect(True)
        self.root.attributes('-transparent', 'black')

        window_width = 400 * 2
        window_height = 500 * 2
        self.root.geometry(f"{window_width}x{window_height}")
        # 获取屏幕的宽度和高度
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # 计算窗口的右下角坐标
        x_position = screen_width - window_width - 50
        y_position = screen_height - window_height - 150
        # 设置窗口位置
        self.root.geometry(f"+{x_position}+{y_position}")
        # 强制设置窗口在最顶层
        self.root.attributes("-topmost", True)
        
        self.tk_widget_config()

        self.app = AppOgl(self.root, width=window_width, height=window_height)
    pass

    def tk_widget_config(self):
        entry = tkinter.Entry(self.root, width=40)
        entry.pack(pady=10)

        def on_confirm_chat_button_click():
            str_user_input = entry.get()
            # def on_finish(str):
                # self.app.chat
                # self.model.StartMotion("Speek", 0, live2d.MotionPriority.FORCE, self.start_speek_callback)
            #     pass
            # asyncio.run(start_chat(str_user_input, on_finish))
            self.app.chat(str_user_input)
            pass
        self.confirm_chat_button = tkinter.Button(self.root, text="确认", command=on_confirm_chat_button_click)
        self.confirm_chat_button.pack()

        pass

    def quit(self):
        live2d.dispose()
        pygame.mixer.quit()
        pass