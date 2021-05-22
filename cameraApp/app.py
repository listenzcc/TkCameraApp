'''
File: app.py
Author: Chuncheng
Version: 0.0
Purpose: Establish the Tkinter App of Camera Displayer
'''

# %%
import cv2

from functools import partial
from PIL import Image, ImageTk

from . import logger
from .cameraDriver import CameraDriver
from .tkLayout import TkWindow

# %%
display_rate = 20  # Hz

# %%

interval = int(1000 / display_rate)


def video_loop(cd, wnd, interval=interval):
    ''' Video Loop of Display on [panel] of [root],
    the frame rate is about 1 / [interval].

    Args:
    - @cd: The CameraDriver instance;
    - @wnd: The Tkinter Window instance;
    - @interval: The interval between frames, default value is 50 milliseconds.
    '''

    wnd.screen.busy = True

    if not cd.state().startswith('Capturing'):
        wnd.screen.busy = False
        wnd.labs['PlayingState']['text'] = 'Holding'
        logger.warning(
            f'Stopped Video Loop since the Camera Driver is not KeepCapturing.')
        return

    cv2image = cv2.cvtColor(cd.img, cv2.COLOR_BGR2RGBA)
    current_image = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=current_image)
    wnd.screen.imgtk = imgtk
    wnd.screen.config(image=imgtk)

    if not wnd.labs['PlayingState']['text'] == 'playing':
        wnd.labs['PlayingState']['text'] = 'Playing'

    # todo: The timing method is incorrect, consider changing it.
    wnd.root.after(interval, video_loop, cd, wnd)


def start(cd, wnd):
    cd.capturing('start')
    if wnd.screen.busy:
        logger.warning(f'Failed Start Video Loop since the Screen is Busy')
    else:
        video_loop(cd, wnd)


def stop(cd):
    cd.capturing('stop')


def connect(cd, wnd):
    if cd.connect():
        wnd.btns['Start']['state'] = 'active'
        wnd.btns['Stop']['state'] = 'active'


def release(cd, wnd):
    cd.release()
    wnd.btns['Start']['state'] = 'disabled'
    wnd.btns['Stop']['state'] = 'disabled'

# %%


def run_app():
    cd = CameraDriver()
    tkwnd = TkWindow()

    def print1(text):
        tkwnd.labs['ConnectionState']['text'] = text

    cd._state_onChange = print1

    tkwnd.btns['Start']['command'] = partial(start, cd, tkwnd)
    tkwnd.btns['Stop']['command'] = partial(stop, cd)
    tkwnd.btns['Start']['state'] = 'disabled'
    tkwnd.btns['Stop']['state'] = 'disabled'
    tkwnd.btns['Connect']['command'] = partial(connect, cd, tkwnd)
    tkwnd.btns['Release']['command'] = partial(release, cd, tkwnd)

    tkwnd.labs['PlayingState']['text'] = 'Holding'

    tkwnd.screen.busy = False

    # tkwnd.btns['Connect']['state'] = 'disabled'

    tkwnd.mainloop()

# %%
