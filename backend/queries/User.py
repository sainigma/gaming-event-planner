import time
from interfaces.QueryInterface import QueryInterface
from utils.Authentication import Authentication

class User(QueryInterface):
    def initialize(self):
        self.auth = Authentication()

    def userExists(self, username):
        query = "select id from users where username = '{0}'".format(str(username))
        result = self.executeQuery(query)
        if (len(result) > 0):
            return True
        return False

    def new(self, username, password):
        if (self.userExists(username)):
            return None
        hashedPassword = self.auth.hash(password)
        query = "insert into users (username, auth) values ('{0}', '{1}');".format(str(username), str(hashedPassword))
        self.executeQuery(query)
        return self.login(username, password)
        
    def login(self, username, password):
        query = "select auth from users where username = '{0}'".format(str(username))
        result = self.executeQuery(query)
        if (len(result) == 0):
            return None
        hashedPassword, salt = result[0][0].split(':')
        testPassword = self.auth.hashWithSalt(password, salt).split(':')[0]
        if (hashedPassword == testPassword):
            token, expires = self.auth.createToken(username)
            tokenQuery = "insert into verifications (bearer, timeout) values ('{0}', '{1}');".format(str(token), str(expires))
            self.executeQuery(tokenQuery)
            return token
        return None

    def find(self, searchstring, username):
        userID = self._getUserID(username)
        subquery = "select relation from userrelations where userid = {0} and type = 1".format(int(userID))
        query = "select id, username from users where id in ({0}) and username like '{1}%'".format(str(subquery), str(searchstring))
        return self.executeQuery(query)

    def relationExists(self, userId, targetId):
        query = "select id from userrelations where userid = {0} and relation = {1}".format(int(userId), int(targetId))
        result = self.executeQuery(query)
        if (len(result) > 0):
            return True
        return False

    def relate(self, username, target, relationType):
        userID = self._getUserID(username)
        targetID = self._getUserID(target)
        if (userID == None or targetID == None):
            return
        if (self.relationExists(userID, targetID)):
            return
        query = "insert into userrelations (userid, relation, type) values ({0}, {1}, {2})".format(int(userID), int(targetID), int(relationType))
        self.executeQuery(query)

    def getFriendRequests(self, username):
        userID = self._getUserID(username)
        subquery = "select relation from userrelations where userid = {0}".format(int(userID))
        query = "select username from userrelations left join users u on userid = u.id where relation = {0} and userid not in ({1})".format(int(userID), str(subquery))
        return self.executeQuery(query)

    def verify(self, bearer):
        token = bearer[7:]
        query = "select timeout from verifications where bearer = '{0}'".format(str(token))
        result = self.executeQuery(query)
        if (len(result) == 0):
            print('Invalid verification')
            return None
        expires = int(result[0][0])
        if (int(time.time()) > expires):
            print('Verification timeout')
            return None
        username = self.auth.getUsername(token)
        return username

    def belongsToGroup(self, userId, groupId):
        if (int(groupId) == -1):
            return True
        query = "select 1 from usergroupregister where userid = {0} and usergroup = {1} and accepted = TRUE and verified = TRUE".format(int(userId), int(groupId))
        result = self.executeQuery(query)
        if (len(result) == 0):
            return False
        return True

    def _getUserID(self, name):
        query = "select id from users where username = '{0}'".format(str(name))
        result = self.executeQuery(query)
        if (len(result) == 0):
            return None
        return result[0][0]