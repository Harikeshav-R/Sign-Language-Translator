#  Copyright (c) 2023 Harikeshav R
#  All rights reserved.

from SpeechToSign.compiler import VideoDisplayer
from SpeechToSign.translator import ISLConverter

sentence = input("> ")
converter = ISLConverter()
video_displayer = VideoDisplayer()

parsed = converter.convert_to_isl(sentence).split()
print(parsed)
video_displayer.show(parsed)
video_displayer.destroy_delayed()
