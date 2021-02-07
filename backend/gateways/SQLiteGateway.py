import sqlite3, os
from gateways.AbstractGateway import AbstractGateway

# Debuggakseen tarkoitettu gateway
class SQLiteGateway(AbstractGateway):

    def initialize(self):
        self.enumValues = {
            'uuid':'integer',
            'int':'integer',
            'timestamp':'date'
        }
        self.connection = sqlite3.connect('./dummy.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        #self.connection.close()

    def enumerate(self, type):
        if type in self.enumValues:
            return self.enumValues[type]
        return type

    def executeQuery(self, query):
        print(query)
        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

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