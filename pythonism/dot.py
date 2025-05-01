#▓▒░▮▯


# 13983

x_ = 30
y_ = 10


#from pynput import keyboard
#from pynput.keyboard import Key
import keyboard
import os
import subprocess
retcode = subprocess.call(['echo', '^[[C'],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT)


def on_key_release(event):
    global x_
    global y_
    if event.name == 'right':
        x_ += 2
        if x_ > 79: x_ = 0
    elif event.name == 'left':
        x_ -= 2
        if x_ < 0: x_ = 79
    elif event.name == 'down':
        y_ += 1
        x_  += 1
        if y_ > 23: y_ = 0
    elif event.name == 'up':
        y_ -= 1
        x_ -= 1
        if y_ < 0: y_ = 23
    draw_screen(x_,y_)


def draw_screen(x_,y_,new=False):
    if not new:
        print('',end='\r')
    print()
    for y in range(24):
        for x in range(79):
            if x <4 and y ==0:
                continue
            if x == x_ and y == y_:
                print('▓', end='')
            else:
                print('░', end='')

draw_screen(x_,y_,new=True)
keyboard.on_press(on_key_release)
keyboard.wait()
#░░░░░░░░░░░░
