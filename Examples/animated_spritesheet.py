# This file was created by Jason Liau
import pygame as pg
# allows us to access information from pygame

FPS = 30

frames = ["Frame1", "Frame2", "Frame3", "Frame4"]

clock = pg.time.Clock()

current_frame = 0
last_update = 0

# creates a function that animates/prints the frame we want to animate and the ticks
def animate():
    global last_update
    global current_frame
    now = pg.time.get_ticks()
    if now - last_update > 350:
        print(frames[current_frame])
        current_frame = (current_frame + 1) % len(frames)
        
        print(now)
        last_update = now

while True:
    clock.tick(FPS)
    animate()