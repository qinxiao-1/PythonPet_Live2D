from Config.resources import *
import tkinter
from TKwindow.tk_window import tkwindow

import asyncio
from OpenAI.openai_custom import *

def start():
    tk = tkwindow()
    tk.app
    tk.app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    tk.app.animate = 1
    tk.app.mainloop()

    tk.quit()
    pass

if __name__ == '__main__':
    start()
    # async test
    # def on_finish(str):
    #     print(str)
    # asyncio.run(start_chat("你好", on_finish))
    # print(request_openai("你好"))
    pass