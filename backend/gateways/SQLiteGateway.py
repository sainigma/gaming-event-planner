import sqlite3, os
from interfaces.GatewayInterface import GatewayInterface

# Debuggakseen tarkoitettu gateway
class SQLiteGateway(GatewayInterface):

    def initialize(self):
        self.enumValues = {
            'uuid':'int',
            'timestamp':'date'
        }
        self.connection = sqlite3.connect('./dummy.db')
        self.cursor = self.connection.cursor()
        self.populate()
        #self.connection.close()

    def enumerate(self, type):
        if type in self.enumValues:
            return self.enumValues[type]
        return type

    def executeQuery(self, query):
        self.cursor.execute(query)

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