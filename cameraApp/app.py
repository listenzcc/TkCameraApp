'''
File: app.py
Author: Chuncheng
Version: 0.0
Purpose: Establish the Tkinter App as Camera Displayer
'''

# %%
import cv2
import numpy as np

from PIL import Image, ImageTk
from tkinter import Tk, Label, Button, Frame, BOTH, RAISED

from . import logger
from .cameraDriver import CameraDriver

# %%
display_rate = 20
title = 'Camera Displayer'
cursor = 'arrow'

# %%
# Init
root = Tk()

# Layout
paddings = dict(padx=10, pady=10)

# Level 0, Root
root.title(title)
root.config(cursor=cursor)

# Level 1, Panels
# Screen Panel
panel1 = Frame(root, relief=RAISED, borderwidth=1)
panel1.pack(fill=BOTH, expand=True, **paddings)

# Control Panel
panel2 = Frame(root, relief=RAISED, borderwidth=1)
panel2.pack(fill=BOTH, expand=True, **paddings)

# Level 2
# Screen
screen = Label(panel1)
screen.pack(**paddings)

# Buttons
btn1 = Button(panel2, text='Connect')
btn1.pack(side='left', **paddings)

btn2 = Button(panel2, text='Release')
btn2.pack(side='left', **paddings)

# %%


def video_loop(cd, root=root, screen=screen, interval=50):
    ''' Video Loop of Display on [panel] of [root],
    the frame rate is about 1 / [interval].

    Args:
    - @cd: The CameraDriver instance;
    - @root: The root object of tkinter;
    - @screen: The screen to display the video;
    - @interval: The interval between frames, default value is 50 milliseconds.
    '''
    if not cd._valid_camera():
        cd.connect()
        cd.capturing('start')
        root.after(100, video_loop, cd)

    cv2image = cv2.cvtColor(cd.img, cv2.COLOR_BGR2RGBA)
    current_image = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=current_image)
    screen.imgtk = imgtk
    screen.config(image=imgtk)

    # todo: The timing method is incorrect, consider changing it.
    root.after(interval, video_loop, cd)


# %%
def run_app():
    cd = CameraDriver()

    # cd.capturing('start')
    video_loop(cd)

    root.mainloop()

    # cd.capturing('stop')

    cd.release()

# %%
