from interfaces.QueryInterface import QueryInterface
from utils.Authentication import Authentication

class User(QueryInterface):
    def initialize(self):
        self.auth = Authentication()

    def new(self, username, password):
        hashedPassword = self.auth.hash(password)
        query = 'insert into users (username, auth) values ("' + username + '", "' + hashedPassword + '");'
        self.executeQuery(query)
        
    def login(self, username, password):
        query = 'select auth from users where username = "' + username + '"'
        result = self.executeQuery(query)
        if (len(result) == 0):
            return None
        hashedPassword, salt = result[0][0].split(':')
        testPassword = self.auth.hashWithSalt(password, salt).split(':')[0]
        if (hashedPassword == testPassword):
            token, expires = self.auth.createToken(username)
            tokenQuery = 'insert into verifications (bearer, timeout) values ("' + token + '", ' + str(expires) + ');'
            self.executeQuery(tokenQuery)
            return token
        return None

    def relate(self, username, target, relationType):
        userID = self._getUserID(username)
        targetID = self._getUserID(target)
        if (userID == None or targetID == None):
            return
        query = 'insert into userrelations (user, relation, type) values ("' + str(userID) + '", "' + str(targetID) + '", "' + str(relationType) + '")'
        self.executeQuery(query)

    def verify(self, username, bearer):
        token = bearer[7:]
        query = 'select timeout from verifications where bearer = "' + token + '"'
        result = self.executeQuery(query)
        if (len(result) == 0):
            return None
        if (True): #timeoutin prosessointi tähän
            return True
        query = 'delete from verifications where bearer = "' + token + '"'
        self.executeQuery(query)
        return None 

    def _getUserID(self, name):
        query = 'select id from users where username = "' + name + '"'
        result = self.executeQuery(query)
        if (len(result) == 0):
            return None
        return result[0][0]