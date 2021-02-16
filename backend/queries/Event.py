from interfaces.QueryInterface import QueryInterface
class Event(QueryInterface):
    def new(self, name, gameId, owner, groupId):
        print(name,gameId,owner,groupId)
        pass
