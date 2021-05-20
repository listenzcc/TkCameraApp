'''
File: tkLayout.py
Author: Chuncheng
Version: 0.0
Purpose: Establish and Layout the Tkinter GUI
'''

from tkinter import Tk, Label, Button, Frame, BOTH, RAISED
from . import logger

title = 'Camera Displayer'
cursor = 'arrow'
paddings = dict(padx=10, pady=10)


class TkWindow(object):
    ''' The Window object of the Tkinter.
    '''

    def __init__(self):
        ''' Initialize the Tkinter Window '''
        root = Tk()
        root.title(title)
        root.config(cursor=cursor)
        self.root = root
        logger.info('Initialized Tkinter Window.')

    def layout(self):
        ''' Setup Layout of the Tkinter Window '''
        # Control Panel
        panel1 = Frame(self.root, relief=RAISED, borderwidth=1)
        panel1.pack(fill=BOTH, expand=True, **paddings)

        # Control Panel
        panel2 = Frame(self.root, relief=RAISED, borderwidth=1)
        panel2.pack(fill=BOTH, expand=True, **paddings)

        self.panel1 = panel1
        self.panel2 = panel2

        logger.info('Setup Layout of the Tkinter Window')

    def components(self):
        ''' Setup Components into the Panels '''
        # Screen
        screen = Label(self.panel1)
        screen.pack(**paddings)

        # Buttons
        btns = dict()

        def add(text, panel=self.panel2):
            btn = Button(panel, text=text)
            btn.pack(side='left', **paddings)
            btns[text] = btn
            logger.debug(f'Added Button of "{text}" into "{panel}"')

        add('Connect')
        add('Release')
        add('Start')
        add('Stop')

        self.btns = btns


tkwnd = TkWindow()
