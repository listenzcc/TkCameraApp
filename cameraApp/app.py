'''
File: app.py
Author: Chuncheng
Date: 2021-05-18
Version: 0.0
Purpose: Establish the Tkinter App as Camera Displayer
'''

# %%
import cv2
from PIL import Image, ImageTk
from tkinter import Tk, Label
from cameraDriver import CameraDriver

# %%
display_rate = 20
title = 'Camera Displayer'
cursor = 'arrow'

# %%
# Init
root = Tk()

# Layout
root.title(title)
root.config(cursor=cursor)

panel = Label(root)
panel.pack(padx=10, pady=10)

# %%


def video_loop(cd, root=root, panel=panel, interval=50):
    ''' Video Loop of Display on [panel] of [root],
    the frame rate is about 1 / [interval].

    Args:
    - @cd: The CameraDriver instance;
    - @root: The root object of tkinter;
    - @panel: The panel to display the video;
    - @interval: The interval between frames, default value is 50 milliseconds.
    '''
    cv2image = cv2.cvtColor(cd.img, cv2.COLOR_BGR2RGBA)
    current_image = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=current_image)
    panel.imgtk = imgtk
    panel.config(image=imgtk)
    root.after(interval, video_loop, cd)


# %%
cd = CameraDriver()

cd.capturing('start')
video_loop(cd)

root.mainloop()

cd.capturing('stop')

cd.release()

# %%
