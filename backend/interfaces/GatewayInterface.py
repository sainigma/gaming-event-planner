from queries.User import User
from queries.Populator import Populator

class GatewayInterface:
    def __init__(self, gameDB):
        self.initialize()
        self.queries = {
            'users':User(self.enumerate, self.executeQuery)
        }
        self.gameDB = gameDB
        Populator(self).populate()

    def newUser(self, username, password):
        self.queries['users'].new(username, password)

    def login(self, username, password):
        return self.queries['users'].login(username, password)

    def executeQuery(self, query):
        # Tietokantapyyntö
        pass

    def enumerate(self, type):
        # Palauttaa enumeraattorin kautta oikean tietuetyypin, structure.jsonissa käytössä psqldatatyypit
        return type

    def initialize(self):
        # Tarkistaa onko tietokanta alustettu
        # Jos ei, alustaa tietokannan
        pass

    def verify(self, key):
        # Autentikaatio
        # Palauttaa 1 jos ok
        # Muutoin -1
        pass