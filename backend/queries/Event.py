import os
from interfaces.QueryInterface import QueryInterface
class Event(QueryInterface):

    def new(self, name, gameId, ownerId, groupId):
        placeholderDescription = 'Placeholder description, edit me!'
        query = 'insert into events (owner, usergroup, name, gameid, description) values ({0}, {1}, "{2}", {3}, "{4}")'.format(int(ownerId), int(groupId), str(name), int(gameId), str(placeholderDescription))
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

    def invite(self, eventId, userId):
        notParticipantQuery = 'select id from eventparticipants where user = {0} and event = {1}'.format(int(userId), int(eventId))
        result = self.executeQuery(notParticipantQuery)
        if (len(result) > 0):
            return
        invitationExistsQuery = 'select id from eventinvites where user = {0} and event = {1}'.format(int(userId), int(eventId))
        result = self.executeQuery(invitationExistsQuery)
        if (len(result) > 0):
            return

        query = 'insert into eventinvites (event, user) values ({0}, {1})'.format(int(eventId), int(userId))
        self.executeQuery(query)

    def _parseInvitation(self, userId, eventId, accepted):
        validInvitationQuery = 'select id from eventinvites where event = {0} and user = {1}'.format(int(eventId), int(userId))
        result = self.executeQuery(validInvitationQuery)
        if (len(result) == 0):
            return
        inviteId = result[0][0]
        forgetInvitationQuery = 'delete from eventinvites where id = {0}'.format(int(inviteId))
        self.executeQuery(forgetInvitationQuery)
        
        if (accepted):
            self.addParticipant(userId, eventId)

    def acceptInvitation(self, userId, eventId):
        self._parseInvitation(userId, eventId, True)

    def declineInvitation(self, userId, eventId):
        self._parseInvitation(userId, eventId, False)

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
        query = 'select id, name from events where id in (select event from eventparticipants where user = {0}) and owner != {0}'.format(int(userId))
        return self._returnEvent(query)