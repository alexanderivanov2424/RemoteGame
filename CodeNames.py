import pygame
from pygame.locals import *
from tkinter import *

from Game import *

class CodeNames(Game):
    def __init__(self):
        super(Game)

    ########### SERVER SIDE ###########
    #update state based on client packet
    def process_packet(self, data, id):
        pass

    ########### CLIENT SIDE ###########
    #render based on current state
    def render(self, screen):
        pass

    #store data about user inputs
    def handle_click(self, mouse_loc):
        pass

    #store data about user inputs
    def handle_press(self, key):
        pass

    #update state based on server response
    def update(self, data):
        pass

    #get data packet to send server
    def get_packet(self):
        pass
