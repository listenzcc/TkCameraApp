'''
File: cameraDriver.py
Author: Chuncheng
Version: 0.0
Purpose: Drive your Camera to Capture the Images.
'''

# %%
import cv2
import time
import threading
import traceback

import numpy as np

from . import logger

frame_rate = 20  # Hz


class CameraDriver(object):
    ''' Operation of the Camera '''

    def __init__(self):
        ''' Initialize the Camera Driver.
        '''
        self.camera = None
        # self.connect()
        logger.info('Initialized Camera Driver.')

    def _valid_camera(self):
        ''' Built-in function of validate the camera object.

        Returns:
        - The boolean value if the camera is valid.
        '''
        if self.camera is None:
            return False
        return True

    def connect(self):
        ''' Connect to the Camera

        Generates:
        - @self.camera: The camera object, the value of None refers to the camera is invalid;
        - @self.img: The latest image.
        '''
        if not self._valid_camera():
            try:
                camera = cv2.VideoCapture(0)
                success, img = camera.read()
                if success:
                    self.camera = camera
                    self.img = img
                    logger.info(
                        f'Connected the Camera, img size is "{img.shape}"')
                else:
                    self.release()
                    logger.error('Failed to Read Image from the Camera.')
            except:
                err = traceback.format_exc()
                self.release()
                logger.error(
                    f'Failed to Connect to the Camera, error is "{err}"')

    def release(self):
        ''' Release the Camera '''
        if not self._valid_camera():
            logger.warning('Invalid Camera.')
            return

        # The camera may be incorrect on releasing
        try:
            self.capturing('stop')
            self.camera.release()
        except:
            err = traceback.format_exc()
            logger.error(f'Incorrect releasing the camera, error is "{err}"')

        self.camera = None
        logger.info('Released Camera.')

    def capturing(self, cmd='start'):
        ''' Capturing by the Camera

        Args:
        - @cmd: 'start' refers starting the camera capturing; 'stop' refers stopping it, default by 'start'.
        '''
        if cmd == 'start':
            t = threading.Thread(target=self.capture, args=('keep',))
            t.setDaemon(True)
            t.start()

        if cmd == 'stop':
            self.keep_capturing = False

    def capture(self, mod='single', frame_rate=frame_rate):
        ''' Capture an image or continuing images using the camera.

        Args:
        - @mod: The mod of the capturing, 'single' for single capture; 'keep' for keep capture, default by 'single';
        - @frame_rate: The frame rate of the capturing.

        Generates:
        - @self.img: The latest image.

        Returns:
        - @img: The latest image, the value will be None if something is wrong.
        '''
        if not self._valid_camera():
            logger.warning('Invalid Camera.')
            return

        if mod == 'single':
            success, img = self.camera.read()
            if not success:
                logger.error('Incorrect Camera.')
                self.release()
                return None

            self.img = img
            logger.info('Finished Single Shot.')
            return img

        if mod == 'keep':
            self.keep_capturing = True
            count = 0
            interval = 1 / frame_rate
            _interval = interval / 2
            logger.info(
                f'Start Keep Capturing, Frame Rate is "{frame_rate} Hz".')

            t0 = time.time()
            while self.keep_capturing:
                success, img = self.camera.read()
                if not success:
                    logger.error('Incorrect Camera.')
                    self.release()
                    break

                self.img = img
                count += 1

                # Report Real Frame Rate Every 10 Seconds
                if count % (frame_rate * 10) == 0:
                    r = count / (time.time() - t0)
                    logger.debug(f'Real frame_rate is "{r}"')

                time.sleep(_interval)

            logger.info(f'Finished Keep Capturing, Captured "{count}" Times.')
            return self.img


# %%
if __name__ == '__main__':
    cd = CameraDriver()
    print(cd.capture().shape)

    cd.capturing('start')
    time.sleep(4)
    cd.capturing('stop')

    cd.release()

# %%
