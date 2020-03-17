import socket
import numpy as np
import pickle
import time

from tkinter import *

import pygame
from pygame.locals import *

from utils import *

port = 9001
MSG_SIZE = 4096

host = socket.gethostname()  # The server's hostname or IP address
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

root = Tk()
Label(root, text="Host").grid(row=0)
Label(root, text="Port").grid(row=1)
input_host = Entry(root)
input_port = Entry(root)
input_host.grid(row=0, column=1)
input_port.grid(row=1, column=1)
def connect(s):
    global host, port
    host = input_host.get()
    port = int(input_port.get())
    root.destroy()
send_button = Button(root, text="Connect",command=lambda:connect(s)).grid(row=2)
root.mainloop()

print("Connecting to ",host,":",port)
s.connect((host, port))

# obj = np.zeros((10,10))
# msg = pickle.dumps(obj)
# s.sendall(msg)
# data = s.recv(MSG_SIZE)
# recovered = pickle.loads(data)
# print(host, " >> ",data)

screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Client")

font = pygame.font.Font('freesansbold.ttf', 15)

Current_Game = None
hubs = []

update_time = 1
time_last_update = time.time() - update_time

def get_hubs():
    global hubs
    msg = pickle.dumps(("ShowHubs",))
    s.sendall(msg)
    data = s.recv(MSG_SIZE)
    hubs = pickle.loads(data)

def new_hub():
    root = Tk()
    listbox = Listbox(root, selectmode=SINGLE)
    listbox.pack()
    for g in GAME_TYPES:
        listbox.insert(END, g.__name__)

    def select():
        if len(listbox.curselection()) == 0:
            return
        game = GAME_TYPES[listbox.curselection()[0]].__name__
        s.sendall(pickle.dumps(("NewHub",game)))
        root.destroy()
    select_button = Button(root, text="OKAY",command=select)
    select_button.pack()
    root.mainloop()

    try:
        status = s.recv(MSG_SIZE)
    except:
        pass

def join_hub(i):
    global Current_Game
    msg = pickle.dumps(("EnterHub",i))
    s.sendall(msg)
    data = s.recv(MSG_SIZE)
    Current_Game = (pickle.loads(data)[0])()

def leave_hub():
    msg = pickle.dumps(("LeaveHub",))
    s.sendall(msg)
    try:
        status = s.recv(MSG_SIZE)
    except:
        pass

def game_communication():
    data = Current_Game.get_packet()
    msg = pickle.dumps((">>",data))
    s.sendall(msg)
    try:
        msg = s.recv(MSG_SIZE)
        packet = pickle.loads(msg)
        Current_Game.update(packet)
    except:
        pass

def render(screen):
    if Current_Game == None:
        screen.fill((255,255,255))
        pygame.draw.rect(screen, (0, 187, 255), (0, 0, screen.get_width(),40))
        text = font.render("Game " + " "*15 + " |  Players   |   Time",False,(0,0,0))
        screen.blit(text,(10,10))

        pygame.draw.rect(screen, (0, 187, 255), (0, screen.get_height()-40, screen.get_width(),40))
        text = font.render("New Hub",False,(0,0,0))
        screen.blit(text,(10, screen.get_height()-30))

        for i,hub in enumerate(hubs):
            pygame.draw.rect(screen, (89, 211, 255), (20, 50 + i*50, screen.get_width()-40,40))
            name = hub.game.__class__.__name__
            TEXT = ''
            TEXT += name + " "*(20 - len(name))
            TEXT += " | " + str(len(hub.users)) + " "*(10 - len(str(len(hub.users))))
            TEXT += " | " + str(hub.time) + " "*(10 - len(str(hub.time)))
            text = font.render(TEXT,False,(0,0,0))
            screen.blit(text,(40, 60 + i*50))
    else:
        Current_Game.render(screen)

def handle_click(mouse_loc):
    if Current_Game == None:
        if 0 < mouse_loc[0] and mouse_loc[0] < screen.get_width():
            if screen.get_height()-40 < mouse_loc[1] and mouse_loc[1] < screen.get_height():
                new_hub()

        for i,hub in enumerate(hubs):
            if 20 < mouse_loc[0] and mouse_loc[0] < screen.get_width()-20:
                if 50 + i*50 < mouse_loc[1] and mouse_loc[1] < 50 + i*50 + 40:
                    join_hub(i)
    else:
        Current_Game.handle_click(mouse_loc)


def handle_press(key):
    global Current_Game
    if Current_Game == None:
        return
    else:
        if key == K_ESCAPE:
            Current_Game = None
            leave_hub()
            return
        Current_Game.handle_press(key)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            s.close()
            break
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_loc = pygame.mouse.get_pos()
            handle_click(mouse_loc)
        if event.type == pygame.KEYUP:
            handle_press(event.key)

    if time.time() - time_last_update > update_time:
        time_last_update = time.time()
        if Current_Game == None:
            get_hubs()
        else:
            game_communication()

    render(screen)
    #pygame.display.update()
    pygame.display.flip()
