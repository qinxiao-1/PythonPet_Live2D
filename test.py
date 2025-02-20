import pygame
import winsound

# 播放 .wav 文件
winsound.PlaySound(r".\Resources\Audio\audio1.wav", winsound.SND_FILENAME)

# 初始化 pygame
# pygame.mixer.init()

# # 加载 .wav 文件
# pygame.mixer.music.load(r".\Resources\Audio\audio1.wav")

# # 播放音频
# pygame.mixer.music.play()

# # 等待音频播放完毕
# while pygame.mixer.music.get_busy():
#     pygame.time.Clock().tick(10)