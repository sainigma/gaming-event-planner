import hashlib, uuid, json, os, time, jwt

class GatewayInterface:
    def __init__(self, gameDB):
        self.entryTypes = {
            'users':self.newUserQuery
        }
        self.secret = os.getenv("SECRET")
        self.gameDB = gameDB
        self.loadStructure()
        self.loadDummy()
        self.initialize()

    def createTableQuery(self, key):
        table = self.structure['tables'][key]
        idtype = 'id ' + self.enumerate(table['id']) + ' primary key' if 'id' in table else 'id ' + self.enumerate('int') + ' primary key'
        query = (
            'create table ' + key + ' ( ' +
            idtype
        )
        for field in table.keys():
            if (field != "id"):
                fiedltType = self.enumerate(table[field])
                query += ', ' + field + ' ' + fiedltType
        query += ' );'
        return query

    def newUserQuery(self, entry):
        hashedPassword = self.hash(entry['password'])
        return 'insert into users (username, auth) values ("' + entry['username'] + '", "' + hashedPassword + '");'

    def newTokenQuery(self, token, timeout):
        return 'insert into verifications (bearer, timeout) values ("' + token + '", ' + str(timeout) + ');'

    def createEntryQuery(self, table, entry):
        if (table in self.entryTypes):
            return self.entryTypes[table](entry)
        return ''

    def populate(self):
        for table in self.structure['tables'].keys():
            query = self.createTableQuery(table)
            self.executeQuery(query)
        for table in self.dummy.keys():
            for entry in self.dummy[table]:
                query = self.createEntryQuery(table, entry)
                self.executeQuery(query)

    def loadStructure(self):
        with open('database/structure.json') as structure:
            self.structure = json.load(structure)

    def loadDummy(self):
        with open('database/dummy.json') as dummy:
            self.dummy = json.load(dummy)

    def executeQuery(self, query):
        # Tietokantapyyntö
        pass

    def enumerate(self, type):
        # Palauttaa enumeraattorin kautta oikean tietuetyypin, structure.jsonissa psqldatatyypit
        return type

    def initialize(self):
        # Tarkistaa onko tietokanta alustettu
        # Jos ei, alustaa tietokannan
        pass

    def verify(self, username, password):
        # Kirjautuminen
        # Palauttaa bearerin jos ok
        # Muutoin -1
        pass

    def verify(self, key):
        # Autentikaatio
        # Palauttaa 1 jos ok
        # Muutoin -1
        pass

    def createToken(self, username):
        expires = int(time.time() + 3600 * 24 * 30)
        payload = {"username":username, "expires":expires}
        token = jwt.encode(payload, self.secret, algorithm="HS256")
        query = self.newTokenQuery(token, expires)
        self.executeQuery(query)
        return token

    def getHashedPassword(self, username):
        query = 'select auth from users where username = "' + username + '"'
        result = self.executeQuery(query)
        if (len(result) == 0):
            return None
        return result[0][0]

    def hashWithSalt(self, target, salt):
        return hashlib.sha256(salt.encode() + target.encode()).hexdigest() + ':' + salt
    
    def hash(self, target):
        salt = uuid.uuid4().hex
        return self.hashWithSalt(target, salt)

    def login(self, username, password):
        hashedPassword, salt = self.getHashedPassword(username).split(':')
        testPassword = self.hashWithSalt(password, salt).split(':')[0]
        if (hashedPassword == testPassword):
            token = self.createToken(username)
            return token
        return None