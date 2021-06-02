'''
FileName: TCPClient.py
Author: Chuncheng
Version: V0.0
Purpose: Establish the TCP Client in Python
'''

import socket
import threading
import traceback

from . import logger, encode, decode

# ------------------------------------------------------------------------------
# Defines


class TCPClient(object):
    ''' TCP Client Object '''

    def __init__(self, IP, port, buffer_size):
        '''
        Method:__init__

        The initialization of the TCPClient object as IP:port

        Args:
        - @self, IP, port, buffer_size

        '''
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        # Connet to IP:port
        IP = str(IP)
        port = int(port)

        client.connect((IP, port))
        name = client.getsockname()

        # Setup client and name
        self.buffer_size = buffer_size
        self.serverIP = IP
        self.client = client
        self.name = name
        self.boxes = None
        logger.info(f'TCP Client is initialized as {name} to {IP}')

        self.session = None

        # Keep listening
        # self.keep_listen()
        thread = threading.Thread(target=self.keep_listen)
        thread.setDaemon(True)
        thread.start()

        pass

    def close(self):
        '''
        Method:close

        Close the session

        Args:
        - @self

        '''
        # Close the client
        self.client.close()

        logger.info(f'Client closed: {self.serverIP}')
        pass

    def keep_listen(self):
        '''
        Method:keep_listen

        Keep listen to the server,
        - Received the message;
        - Send the message;
        - Auto close if it receives empty message or occurs errors.

        Args:
        - @self

        '''

        logger.info(f'Start listening to {self.serverIP}')

        # thread = threading.Thread(target=self._keep_send_keepAliveMessages)
        # thread.setDaemon(True)
        # thread.start()

        while True:
            try:
                # ----------------------------------------------------------------
                # Wait until new message is received
                income = self.client.recv(self.buffer_size)

                if income == b'':
                    logger.debug('Received empty message')
                    break

                logger.debug(f'Received message of length "{len(income)}"')

                boxes = []
                print(income)
                for bytes in income.split(b'\n'):
                    if len(bytes.strip()) == 0:
                        continue
                    name, p, cx, cy, w, h = bytes.split(b', ')
                    box = dict(name=name.decode(),
                               p=float(p),
                               cx=int(float(cx)),
                               cy=int(float(cy)),
                               w=int(float(w) / 2),
                               h=int(float(h) / 2))
                    boxes.append(box)
                self.boxes = boxes
                logger.debug(f'Boxes has been made.')

            except KeyboardInterrupt:
                logger.error(f'Keyboard Interruption is detected')
                break

            except ConnectionResetError as err:
                logger.warning(
                    f'Connection reset occurs. It can be normal when server closes the connection.')
                break

            except Exception as err:
                detail = traceback.format_exc()
                print(f'E: {detail}')
                logger.error(f'Unexpected error: {err}')
                logger.debug(f'Unexpected error detail: {detail}')
                self.send(
                    f'Connection will be reset due to the undefined problems "{err}", detail is "{detail}"')
                break

        self.close()
        logger.info(f'Stopped listening to {self.serverIP}')

        pass

    def send(self, message):
        '''
        Method:send

        Send [message] to the server.

        Args:
        - @self, message:

        '''
        msg = encode(message)
        self.client.sendall(msg)
        logger.debug(f'Sent msg of Length "{len(msg)}" to {self.serverIP}')

        pass
