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

    def verify(self, username, bearer):
        token = bearer # poista bearerosuus
        query = 'select timeout from verifications where bearer = "' + token + '"'
        result = self.executeQuery(query)
        if (len(result) == 0):
            return None
        # prosessoi