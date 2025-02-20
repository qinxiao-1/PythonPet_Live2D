#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/24 14:30
# @Author  : yhw
# @File    : WavToMp3.py
# @Description :

from pydub import AudioSegment
song = AudioSegment.from_wav("demo.wav")
song.export("demo.mp3", format="mp3")