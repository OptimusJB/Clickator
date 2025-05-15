from Accueil import Accueil
class State:
    def __init__(self):
        self.state_actuel = Accueil(self)

state = State()