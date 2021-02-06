import hashlib, uuid, json

class GatewayInterface:
    def __init__(self, gameDB):
        self.entryTypes = {
            'users':self.newUser
        }
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

    def newUser(self, entry):
        # TODO testaa ensin onko käyttäjä olemassa
        hashedPassword = self.hash(entry['password'])
        return 'insert into users (username, auth) values ("' + entry['username'] + '", "' + hashedPassword + '");'

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

    def hashWithSalt(self, target, salt):
        return hashlib.sha256(salt.encode() + target.encode()).hexdigest() + ':' + salt
    
    def hash(self, target):
        salt = uuid.uuid4().hex
        return self.hashWithSalt(target, salt)

    def login(self, username, password):
        hashedPassword, salt = self.getHashedPassword(username).split(':')
        return hashedPassword == self.hashWithSalt(password, salt)