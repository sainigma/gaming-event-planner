import sqlite3, os
from interfaces.GatewayInterface import GatewayInterface

# Debuggakseen tarkoitettu gateway
class SQLiteGateway(GatewayInterface):

    def initialize(self):
        exists = -1
        if (os.path.isfile('dummy.db')):
            exists = 1
        connection = sqlite3.connect('./dummy.db')
        self.populate(connection)
        connection.close()
        pass

    def populate(self, connection):
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