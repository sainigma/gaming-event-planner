import hashlib, uuid, json

class GatewayInterface:
    def __init__(self):
        self.salt = uuid.uuid4().hex
        self.loadStructure()
        self.loadDummy()
        self.initialize()

    def loadStructure(self):
        with open('database/structure.json') as structure:
            self.structure = json.load(structure)

    def loadDummy(self):
        with open('database/dummy.json') as dummy:
            self.dummy = json.load(dummy)

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

    def hash(self, target):
        return hashlib.sha512(target + self.salt).hexdigest()

    def login(self, username, password):
        hashedPassword = hash(password)
        result = self.verify(username, hashedPassword)
        return result