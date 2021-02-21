import time
from interfaces.QueryInterface import QueryInterface
class Comment(QueryInterface):
    def new(self, eventId, targetId, userId, content):
        # tarkista että targetid on -1 tai löytyy kommenttiketjusta
        # plus muu sanitycheck
        query = 'insert into comments (user, event, target, content, time) \
            values ({0}, {1}, {2}, "{3}", {4})' \
            .format(
                int(userId),
                int(eventId),
                int(targetId),
                str(content),
                int(time.time())
            )
        self.executeQuery(query)
    
    def get(self, eventId):
        query = 'select id, user, event, target, content, time from comments where event = {0} order by time asc'.format(int(eventId))
        result = self.executeQuery(query)
        if (len(result) > 0):
            return result
        return []