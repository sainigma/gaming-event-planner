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
        ownerId = self.queries['users']._getUserID(owner)
        if (self.queries['users'].belongsToGroup(ownerId, groupId)):
            self.queries['events'].new(name, gameId, ownerId, groupId)

    def getEvent(self, eventId):
        event = {}
        event['owner'] = self.queries['events'].getOwner(eventId)
        event['info'] = self.queries['events'].getInfo(eventId)
        event['participants'] = self.queries['events'].getParticipants(eventId)
        return event

    def getEvents(self, username):
        userId = self.queries['users']._getUserID(username)
        
        events = {}
        
        events['my'] = self.queries['events'].getEventsByUser(userId)
        events['attending'] = self.queries['events'].getParticipating(userId)
        events['invites'] = self.queries['events'].getInvitations(userId)

        return events

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