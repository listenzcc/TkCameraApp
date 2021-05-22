'''
File: tkLayout.py
Author: Chuncheng
Version: 0.0
Purpose: Establish and Layout the Tkinter GUI
'''

from functools import partial
from tkinter import Tk, Label, Button, Frame, Text, BOTH, RAISED

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

        self.layout()

    def mainloop(self):
        ''' Start Main Loop for the Tkinter Window '''
        self.root.mainloop()

    def layout(self):
        ''' Layout Pipeline for the Tkinter Window '''
        self.frames()
        self.components()
        logger.info('Finish Layout Pipeline for the Tkinter Window')

    def frames(self):
        ''' Setup Frames of the Tkinter Window '''
        # Control Frame
        frame1 = Frame(self.root, relief=RAISED, borderwidth=1)
        frame1.pack(fill=BOTH, expand=True, **paddings)
        logger.debug(f'Added Frame of "{frame1}".')

        # Info Frame
        frame2 = Frame(self.root, relief=RAISED, borderwidth=1)
        frame2.pack(fill=BOTH, expand=True, **paddings)
        logger.debug(f'Added Frame of "{frame2}".')

        # Control Frame
        frame3 = Frame(self.root, relief=RAISED, borderwidth=1)
        frame3.pack(fill=BOTH, expand=True, **paddings)
        logger.debug(f'Added Frame of "{frame3}".')

        self.frame1 = frame1
        self.frame2 = frame2
        self.frame3 = frame3
        logger.info('Setup Layout of the Tkinter Window')

    def components(self):
        ''' Setup Components into the Panels '''
        # Screen
        screen = Label(self.frame1)
        screen.pack(**paddings)
        logger.debug(f'Added screen of "{screen}"')

        # Info
        labs = dict()

        def add(text, frame=self.frame2):
            lab = Label(frame, text=text)
            lab.pack(side='left', **paddings)
            labs[text] = lab
            logger.debug(f'Added Label of "{text}" into "{frame}"')

        add('ConnectionState')
        add('PlayingState')

        # Buttons
        btns = dict()

        def add(text, frame=self.frame3):
            btn = Button(frame, text=text)
            btn.pack(side='left', **paddings)
            btns[text] = btn
            logger.debug(f'Added Button of "{text}" into "{frame}"')

        add('Connect')
        add('Release')
        add('Start')
        add('Stop')

        self.screen = screen
        self.btns = btns
        self.labs = labs
        logger.info('Setup Components of the Tkinter Window')
