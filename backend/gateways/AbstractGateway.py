from queries.User import User
from queries.Event import Event
from queries.Populator import Populator
from queries.Game import Game
from queries.Comment import Comment

class AbstractGateway:
    def __init__(self):
        self.initialize()
        self.queries = {
            'users':User(self.enumerate, self.executeQuery),
            'events':Event(self.enumerate, self.executeQuery),
            'games':Game(self.enumerate, self.executeQuery),
            'comments':Comment(self.enumerate, self.executeQuery)
        }
        Populator(self).populate()

    def mapResult(self, result, labels):
        for i in range(0, len(result)):
            result[i] = dict(zip(labels, result[i]))
        return result

    def getComments(self, username, eventId):
        # tarkista että käyttäjä osa tapahtumaa
        labels = ['id', 'user', 'event', 'target', 'content', 'time']
        comments = self.queries['comments'].get(eventId)
        if (len(comments) > 0):
            return self.mapResult(comments, labels)
        return []

    def addComment(self, username, content, eventId, targetId):
        # tarkista että käyttäjä osa tapahtumaa
        userId = self.queries['users']._getUserID(username)
        self.queries['comments'].new(eventId, targetId, userId, content)
        # jos kommentin lisääminen onnistui, lähetä socketkäsky klinuille uusista kommenteista

    def findGames(self, searchstring):
        return self.queries['games'].findGames(searchstring)

    def getGame(self, gameId):
        return self.queries['games'].getGame(gameId)

    def parseInvitations(self, username, eventId, invitationStatus):
        print('invitation status:',invitationStatus)
        userId = self.queries['users']._getUserID(username)
        if (int(invitationStatus) == 1):
            self.queries['events'].acceptInvitation(userId, eventId)
        elif (int(invitationStatus) == 0):
            self.queries['events'].declineInvitation(userId, eventId)
        
    def searchUsers(self, searchstring, username):
        users = self.queries['users'].find(searchstring, username)
        return self.mapResult(users, ['id', 'name'])
        # for i in range(0, len(users)):
        #    users[i] = dict(zip(['id', 'name'], users[i]))
        # return users

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

    def inviteToEvent(self, username, targetuser, eventId):
        if (self.queries['events'].getOwner(eventId) == username):
            targetUserId = self.queries['users']._getUserID(targetuser)
            self.queries['events'].invite(eventId, targetUserId)

    def newUser(self, username, password):
        self.queries['users'].new(username, password)

    def newRelation(self, user, target, relationType):
        self.queries['users'].relate(user, target, relationType)

    def login(self, username, password):
        return self.queries['users'].login(username, password)

    def verify(self, bearer):
        return self.queries['users'].verify(bearer)

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