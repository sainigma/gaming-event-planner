import time
from interfaces.QueryInterface import QueryInterface
class Comment(QueryInterface):
    def new(self, eventId, targetId, userId, content):
        # tarkista että targetid on -1 tai löytyy kommenttiketjusta
        # plus muu sanitycheck
        query = "insert into comments (userid, event, target, content, time) \
            values ({0}, {1}, {2}, '{3}', {4})" \
            .format(
                int(userId),
                int(eventId),
                int(targetId),
                str(content),
                int(time.time())
            )
        self.executeQuery(query)
    
    def get(self, eventId):
        query = "select u.username, c.event, c.target, c.content, c.time from comments c left join users u on c.userid = u.id where event = {0}".format(int(eventId))
        result = self.executeQuery(query)
        if (len(result) > 0):
            return result
        return []