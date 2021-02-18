import os
from interfaces.QueryInterface import QueryInterface
class Event(QueryInterface):

    def new(self, name, gameId, ownerId, groupId):
        query = 'insert into events (owner, usergroup, name, gameid) values ({0}, {1}, "{2}", {3})'.format(int(ownerId), int(groupId), str(name), int(gameId))
        if (self.usesPSQL):
            query += ' returning id'
            result = self.executeQuery(query)
        elif (self.usesSQLITE):
            self.executeQuery(query)
            result = self.executeQuery('select max(id) from events')
        else:
            print('missing sql')
            return

        eventId = result[0][0]
        self.addParticipant(ownerId, eventId)

    def getOwner(self, eventId):
        query = 'select username from users where id = (select owner from events where id = {0})'.format(int(eventId))
        return self.executeQuery(query)[0][0]

    def getInfo(self, eventId):
        query = 'select name, description, usergroup, gameid, created, timeout, optupper, optlower from events where id = {0}'.format(int(eventId))
        return self.executeQuery(query)[0]

    def getParticipants(self, eventId):
        query = 'select username from users where id in (select user from eventparticipants where event = {0})'.format(int(eventId))
        return self.executeQuery(query)

    def _returnEvent(self, query):
        result = self.executeQuery(query)
        if (len(result) == 0):
            return []
        return result

    def addParticipant(self, userId, eventId):
        query = 'insert into eventparticipants (user, event) values ({0}, {1})'.format(int(userId), int(eventId))
        self.executeQuery(query)

    def getEventsByUser(self, userId):
        query = 'select id, name from events where owner = {0}'.format(int(userId))
        return self._returnEvent(query)

    def getInvitations(self, userId):
        query = 'select id, name from events where id in (select event from eventinvites where user = {0})'.format(int(userId))
        return self._returnEvent(query)

    def getParticipating(self, userId):
        query = 'select id, name from events where id in (select event from eventparticipants where user = {0})'.format(int(userId))
        return self._returnEvent(query)