import socket               # Import socket module
import _thread
import numpy as np
import pickle

import pygame
from pygame.locals import *

from utils import *

PORT = 9001
MSG_SIZE = 4096

USR_ID = 1

hubs = [] #list of current games
users = [] #list of users

hubs.append(Hub(Chat()))

def host_client(clientsocket,addr, ID):
    usr = User(ID)
    users.append(usr)
    try:
        while True:
            msg = clientsocket.recv(MSG_SIZE)
            try:
                obj = pickle.loads(msg)
                if not type(obj) == tuple:
                    msg = pickle.dumps(('Error','Recieved a non tuple type'))
                    clientsocket.send(msg)
                    continue
            except:
                print("ERROR")

            code = obj[0]
            if code == "ShowHubs":
                ret = hubs
            if code == "NewHub":
                game = Chat
                for g in GAME_TYPES:
                    if g.__name__ == obj[1]:
                        game = g

                if game == None:
                    ret = ('Error','No such game')
                else:
                    hubs.append(Hub(game()))
                    ret = ('Good','Game added')

            if code == "EnterHub":
                hub = hubs[obj[1]]
                hub.users.append(usr)
                usr.hub = hub
                ret = (hub.game.__class__,)

            if code == "LeaveHub":
                usr.hub = None
                for hub in hubs:
                    if usr in hub.users:
                        hub.users.remove(usr)
                        ret = ('Good','Left Hub')
                        break
                ret = ('Error','Not in Hub')

            if code == ">>":
                ret = usr.hub.game.process_packet(obj[1],usr.id)
            clientsocket.send(pickle.dumps(ret))
    except:
        import sys
        print(sys.exc_info())
    finally:
        for hub in hubs:
            if usr in hub.users:
                hub.users.remove(usr)
        clientsocket.close()
        users.remove(usr)

def run_window(s):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                s.close()
                break

        screen.fill((100,100,100))
        #pygame.display.update()
        pygame.display.flip()



pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Server")

s = socket.socket()
_thread.start_new_thread(run_window,(s,))

host = socket.gethostname()

s.bind((host, PORT))
s.listen()
print('Server started!')
print('Waiting for clients...')

while True:
    try:
        c, addr = s.accept()
        print('Got connection from', addr)
        _thread.start_new_thread(host_client,(c,addr, USR_ID))
        USR_ID += 1
    except:
        break
