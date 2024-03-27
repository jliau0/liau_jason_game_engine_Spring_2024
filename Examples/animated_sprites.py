# This file was created by Jason Liau and informed by Aayush
import time
# allows us to access time
import pygame as pg
# allows us to access information from pygame's library

frames = ["Frame1", "Frame2", "Frame3", "Frame4"]
# creates list of our frames

idx = 0
# # creates index to loop through frames
while True:
#     # starts the loop
    time.sleep(1)
#     # creates a 1 second pause
    print(frames[idx])
#     # prints our frames
    idx = (idx + 1) % len(frames)