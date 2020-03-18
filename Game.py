
class Hub:
    def __init__(self, game):
        self.game = game
        self.game.hub = self

        self.users = [] #list of users
        self.time = -1

class User:
    def __init__(self, id):
        self.id = id
        self.name = "Flake " + str(id)
        self.hub = None

class Game:
    def __init__(self):
        self.hub = None

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
