'''
FileName: TCPUI.py
Author: Chuncheng
Version: V0.0
Purpose: The UI of the TCP Socket
'''

import sys

from .TCPServer import TCPServer
from .TCPClient import TCPClient

kwargs = dict(
    IP='localhost',
    port=33765,
    buffer_size=1024
)

if __name__ == '__main__':
    assert(len(sys.argv) > 1)

    opt = sys.argv[1]

    if opt == 'client':
        client = TCPClient(**kwargs)
        while True:
            cmd = input('>> ')

            if cmd == 'q':
                break

            if cmd.startswith('send '):
                client.send(cmd[5:])

    if opt == 'server':
        server = TCPServer(**kwargs)
        server.start()
        while True:
            cmd = input('>> ')

            if cmd == 'q':
                break

            if cmd.startswith('send '):
                for session in server.alive_sessions():
                    session.send(cmd[5:])

            if cmd == 'list':
                print(server.alive_sessions())
