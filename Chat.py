import pygame
from pygame.locals import *
from tkinter import *

from Game import *

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 15)

class Chat(Game):
    def __init__(self):
        super(Game)

        self.updates = {}

        self.queue = [] #user send queue
        self.messages = [] #messages in chat

    ########### SERVER SIDE ###########
    #update state based on client packet
    def process_packet(self, data, id):
        if not id in self.updates.keys():
            self.updates[id] = []

        name = str(id)
        for usr in self.hub.users:
            if usr.id == id:
                name = usr.name

        for k in self.updates.keys():
            for msg in data:
                self.updates[k].append((name,msg))

        ret = self.updates[id]
        self.updates[id] = []
        return ret

    ########### CLIENT SIDE ###########
    #render based on current state
    def render(self, screen):
        screen.fill((255,255,255))
        for i, msg in enumerate(self.messages):
            text = font.render(msg[0] + ": " + msg[1],False,(0,0,0))
            screen.blit(text,(20, 60 + i*30))

    #store data about user inputs
    def handle_click(self, mouse_loc):
        root = Tk()
        input = Entry(root)
        input.pack()
        def send(self):
            if len(input.get()) == 0:
                return
            self.queue.append(input.get())
            root.destroy()
        send_button = Button(root, text="OKAY",command=lambda:send(self))
        send_button.pack()
        root.mainloop()

    #store data about user inputs
    def handle_press(self, key):
        pass

    #update state based on server response
    def update(self, data):
        for msg in data:
            self.messages.append(msg)

    #get data packet to send server
    def get_packet(self):
        ret = self.queue
        self.queue = []
        return ret
