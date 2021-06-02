'''
File: app.py
Author: Chuncheng
Version: 0.0
Purpose: Establish the Tkinter App of Camera Displayer
'''

# %%
import io
import os
import sys
import cv2

from functools import partial
from PIL import Image, ImageTk

from . import logger
from .cameraDriver import CameraDriver
from .tkLayout import TkWindow

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'TCPSocket'))  # noqa
from TCPSocket.TCPClient import TCPClient

# %%
display_rate = 20  # Hz

# %%
kwargs = dict(
    IP='172.18.116.144',
    port=33765,
    buffer_size=1024  # 00000
)
client = TCPClient(**kwargs)

# %%

interval = int(1000 / display_rate)

kwargs = dict(
    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    fontScale=1,
    color=(255, 0, 0),
    thickness=2
)


def video_loop(cd, wnd, interval=interval):
    ''' Video Loop of Display on [panel] of [root],
    the frame rate is about 1 / [interval].

    Args:
    - @cd: The CameraDriver instance;
    - @wnd: The Tkinter Window instance;
    - @interval: The interval between frames, default value is 50 milliseconds.
    '''

    wnd.screen.busy = True
    wnd.screen.count += 1

    if not cd.state().startswith('Capturing'):
        wnd.screen.busy = False
        wnd.screen.count = 0
        wnd.labs['PlayingState']['text'] = 'Holding'
        logger.warning(
            f'Stopped Video Loop since the Camera Driver is not KeepCapturing.')
        return

    cv2image = cv2.cvtColor(cd.img, cv2.COLOR_BGR2RGBA)

    if client.boxes is not None:
        for box in client.boxes:
            cx = box['cx']
            cy = box['cy']
            w = box['w']
            h = box['h']
            name = box['name']
            cv2image = cv2.rectangle(
                cv2image, (cx-w, cy-h), (cx+w, cy+h), (0, 0, 0), 2)

            cv2image = cv2.putText(cv2image, name, org=(cx-w, cy-h), **kwargs)

    current_image = Image.fromarray(cv2image)

    if wnd.screen.count > 10:
        wnd.screen.count = 0
        buf = io.BytesIO()
        current_image.save(buf, format='png')
        bytes = buf.getvalue()
        print(len(bytes))
        # print(buf.getvalue()[:10])
        client.send(bytes)

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
    tkwnd.screen.count = 0

    # tkwnd.btns['Connect']['state'] = 'disabled'

    tkwnd.mainloop()

# %%
