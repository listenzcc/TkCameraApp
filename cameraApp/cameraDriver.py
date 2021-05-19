'''
File: cameraDriver.py
Author: Chuncheng
Date: 2021-05-18
Version: 0.0
Purpose: Drive your Camera to Capture the Images.
'''

# %%
import cv2
import time
import threading

frame_rate = 20  # Hz


class CameraDriver(object):
    ''' Operation of the Camera '''

    def __init__(self):
        ''' Initialize the Camera Driver

        Generates:
        - @self.camera: The camera object, the value of None refers to the camera is invalid;
        - @self.img: The latest image.
        '''
        camera = cv2.VideoCapture(0)
        success, img = camera.read()
        if success:
            print(
                f'I: Success Init the Camera, img size is "{img.shape}"')
            self.camera = camera
            self.img = img
        else:
            print('E: Failed Init the Camera.')
            self.camera = None

    def release(self):
        ''' Release the Camera '''
        if self.camera is None:
            print('E: No Camera is Specified.')
            return

        self.camera.release()
        print('I: Camera is Released.')

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
        if mod == 'single':
            if self.camera is None:
                print('E: No Camera is Specified.')

            success, img = self.camera.read()
            if not success:
                print('E: Invalid Camera is Called.')
                self.camera = None
                return None

            self.img = img
            print('I: Finished Single Shot.')
            return img

        if mod == 'keep':
            self.keep_capturing = True
            count = 0
            interval = 1 / frame_rate
            print(f'I: Start Keep Capturing, Frame Rate is "{frame_rate} Hz".')

            t0 = time.time()
            t = time.time()
            while self.keep_capturing:
                # Make sure capturing every [interval] seconds
                if time.time() - t < interval:
                    continue
                else:
                    t = time.time()

                success, img = self.camera.read()
                if not success:
                    print('E: Invalid Camera is Used.')
                    self.camera = None
                    break

                self.img = img
                count += 1

                # Report Real Frame Rate Every 10 Seconds
                if count % (frame_rate * 10) == 0:
                    r = count / (time.time() - t0)
                    print(f'D: Real frame_rate is "{r}"')

            print(f'I: Finished Keep Capturing, Captured "{count}" Times.')
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
