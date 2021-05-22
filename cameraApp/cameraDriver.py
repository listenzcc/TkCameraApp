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

from . import logger

frame_rate = 20  # Hz


class CameraDriver(object):
    ''' Operation of Camera '''

    def __init__(self):
        ''' Initialize Camera Driver  '''
        self.camera = None
        self.keep_capturing = False
        logger.info('Initialized Camera Driver.')

        self._state_onChange = print
        self.state('Disconnected')

    def state(self, _state=None):
        ''' Set or Get State,
        the _state is None refers to Get the State;
        others refers to Set the State.

        Args:
        - @_state: THe State to be Set, default value is None.

        Generates:
        - @self._state: The Inner State;
        - @self._state_onChange: The Method being Called on State Changed.
        '''
        if _state is None:
            return self._state
        else:
            self._state = _state
            self._state_onChange(_state)
            logger.debug(f'Changed State to "{_state}".')

    def connect(self):
        ''' Connect to Camera

        Generates:
        - @self.camera: Camera object, the value of None refers to Camera is invalid;
        - @self.img: The latest image.

        Returns:
        - If the Connecting Operation is successful.
        '''
        if self.camera is None:
            try:
                camera = cv2.VideoCapture(0)
                success, img = camera.read()
                if success:
                    self.camera = camera
                    self.img = img
                    logger.info(
                        f'Connected Camera, img size is "{img.shape}".')
                    self.state('Connected')
                    return True
                else:
                    self.release()
                    logger.error('Failed Read Image from Camera.')
            except:
                err = traceback.format_exc()
                self.release()
                logger.error(
                    f'Failed to Connect to Camera, error is "{err}"')
                return False

        return False

    def release(self):
        ''' Release Camera '''
        if self.camera is None:
            logger.error('Failed Release Camera, since it is Already None.')
            self.state('Disconnected')
            return

        # Camera may be Raising Errors
        self.capturing('stop')
        try:
            self.camera.release()
        except:
            err = traceback.format_exc()
            logger.error(f'Failed Release Camera, error is "{err}".')

        self.camera = None
        self.state('Disconnected')
        logger.info('Released Camera.')

    def capturing(self, cmd='start'):
        ''' Capturing by Camera

        Args:
        - @cmd: 'start' refers starting Camera capturing; 'stop' refers stopping it, default by 'start'.
        '''
        if cmd == 'start':
            # Pervent Repeat Capturing
            if self.state().startswith('Capturing'):
                logger.warning('Can not Repeat Start Capturing.')
                return

            t = threading.Thread(target=self.capture, args=('keep',))
            t.setDaemon(True)
            t.start()

        if cmd == 'stop':
            self.state('Connected')

    def capture(self, mod='single', frame_rate=frame_rate):
        ''' Capture an image or continuing images using Camera.

        Args:
        - @mod: The mod of the capturing, 'single' for single capture; 'keep' for keep capture, default by 'single';
        - @frame_rate: The frame rate of the capturing.

        Generates:
        - @self.img: The latest image.

        Returns:
        - @img: The latest image, the value will be None if something is wrong.
        '''
        if self.camera is None:
            logger.error('Failed Capture Camera, since it is None.')
            return

        if mod == 'single':
            success, img = self.camera.read()
            if not success:
                logger.error(
                    'Failed Single Capture, since Read Camera is Failed.')
                self.release()
                return None

            self.img = img
            logger.info('Finished Single Capture.')
            return img

        if mod == 'keep':
            self.state('Capturing')
            count = 0
            interval = 1 / frame_rate
            _interval = interval / 2
            logger.info(
                f'Start Keep Capturing, Frame Rate is "{frame_rate} Hz".')

            t0 = time.time()
            while self.state().startswith('Capturing'):
                if self.camera is None:
                    logger.error(
                        'Interrupted Keep Capturing, since Camera is None.')
                    self.release()
                    break

                success, img = self.camera.read()
                if not success:
                    logger.error(
                        'Interrupted Keep Capturing, since Read Camera is Failed.')
                    self.release()
                    break

                self.img = img
                count += 1

                # Report Real Frame Rate Every 10 Seconds
                if count > 100:
                    t = time.time()
                    r = count / (t - t0)
                    t0 = t
                    count = 0
                    logger.debug(
                        f'Real frame_rate of the latest 100 capture is "{r}"')
                    self.state(f'Capturing at {r:0.2f} Hz')

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
