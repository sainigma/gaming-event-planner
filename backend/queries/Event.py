from interfaces.QueryInterface import QueryInterface
class Event(QueryInterface):

    def new(self, name, gameId, ownerId, groupId):
        query = 'insert into events (owner, usergroup, name, gameid) values ({0}, {1}, "{2}", {3})'.format(int(ownerId), int(groupId), str(name), int(gameId))
        self.executeQuery(query)

    def getEvents(self, userId):
        query = 'select id, name from events where owner = {0}'.format(int(userId))
        result = self.executeQuery(query)
        if (len(result) == 0):
            return []
        return result
