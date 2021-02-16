from queries.User import User
from queries.Event import Event
from queries.Populator import Populator

class AbstractGateway:
    def __init__(self, gameDB):
        self.initialize()
        self.queries = {
            'users':User(self.enumerate, self.executeQuery),
            'events':Event(self.enumerate, self.executeQuery)
        }
        self.gameDB = gameDB
        Populator(self).populate()

    def newEvent(self, name, gameId, owner, groupId):
        print('jee')
        pass
        self.queries['events'].new(name, gameId, owner, groupId)

    def newUser(self, username, password):
        self.queries['users'].new(username, password)

    def newRelation(self, user, target, relationType):
        self.queries['users'].relate(user, target, relationType)

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

    def verify(self, bearer):
        return self.queries['users'].verify(bearer)