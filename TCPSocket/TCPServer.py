'''
FileName: TCPServer.py
Author: Chuncheng
Version: V0.0
Purpose: Establish the TCP Server in Python
'''

import socket
import threading
import traceback

from . import logger, encode, decode


# ------------------------------------------------------------------------------
# Defines

class TCPServer(object):
    ''' TCP Server Object '''

    def __init__(self, IP, port, buffer_size):
        '''
        Method:__init__

        The initialization of the TCPServer object as IP:port

        Args:
        - @self, IP, port, buffer_size

        '''
        # The handler as the server
        self.server = None

        # The client sessions
        self.sessions = []

        self.buffer_size = buffer_size
        self.IP = str(IP)
        self.port = int(port)

        pass

    def alive_sessions(self):
        '''
        Method:alive_sessions

        Remove disconnected sessions and return the remains

        Args:
        - @self

        Outputs:
        - The alive sessions

        '''
        n = len(self.sessions)
        self.sessions = [e for e in self.sessions if e.is_connected]
        logger.debug('There are {} alive sessions, squeezed from {}'.format(
            len(self.sessions), n))
        return self.sessions

    def start(self):
        '''
        Method:start

        The pipeline of starting the server

        Args:
        - @self

        '''
        self.bind()
        self.serve()
        pass

    def bind(self):
        '''
        Method:bind

        Bind the server to IP:port

        Args:
        - @self

        '''
        if self.server is not None:
            logger.error(f'TCP server has been established: {self.server}')
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.IP, self.port))
        self.server = server
        logger.info(f'TCP server binds on {self.IP}:{self.port}')
        pass

    def serve(self):
        '''
        Method:serve

        Start serving of the TCP Server

        Args:
        - @self

        '''
        # Listen
        self.server.listen(1)
        logger.info(f'TCP server is listening')

        # Generate thread
        thread = threading.Thread(target=self.new_session,
                                  name='TCP session interface')
        thread.setDaemon(True)
        thread.start()
        logger.info(f'TCP server is ready for new session')
        pass

    def new_session(self):
        '''
        Method:new_session

        Handle the in-comming sessions

        Args:
        - @self

        '''
        try:
            while True:
                client, address = self.server.accept()
                session = TCPSession(
                    client=client, address=address, buffer_size=self.buffer_size)
                session.send('Hello from server')
                print(f'New session established: {client} at {address}')
                self.sessions.append(session)
                self.alive_sessions()

        except:
            err = traceback.format_exc()
            logger.fatal(
                f'The new_session threading is stopped due to: "{err}"')

        pass


class TCPSession(object):
    ''' The Session of TCP Server '''

    def __init__(self, client, address, buffer_size):
        '''
        Method:__init__

        The initialization of the TCP session (connected to the TCP client):
        - Setup the session;
        - Mark the is_connected to True.

        Args:
        - @self, client, address:
        - @client: The client object connecting to;
        - @address: The address of the client.

        '''

        self.client = client
        self.address = address
        self.buffer_size = buffer_size
        self.start()
        self.is_connected = True
        logger.info(f'Client connected: {self.address}')

        pass

    def start(self):
        '''
        Method:start

        Start the handling of the TCP session

        Args:
        - @self

        '''

        thread = threading.Thread(
            target=self.handle, name='TCP session handler')
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

        self.client.close()
        self.is_connected = False

        logger.info(f'Client closed: {self.address}')

        pass

    def handle(self):
        '''
        Method:handle

        Handle the message from the client

        Args:
        - @self

        '''

        while True:
            try:
                # ----------------------------------------------------------------
                # Receive new incoming message
                income = self.client.recv(self.buffer_size)
                logger.debug(f'Received {income} from {self.address}')

                # ----------------------------------------------------------------
                # Terminating commands
                if income == b'':
                    self.close()
                    break

            except ConnectionResetError as err:
                logger.error(f'Connection reset occurs. It can be normal.')
                break

            except:
                err = traceback.format_exc()
                logger.error(f'Unexpected error: "{err}"')
                break

        self.close()

        pass

    def send(self, message):
        '''
        Method:send

        Send [message] through the session to the client

        Args:
        - @self, message

        '''

        msg = encode(message)
        self.client.sendall(msg)
        logger.debug(f'Sent "{message}" to {self.address}')

        pass
