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
        self.debug = os.getenv('DEBUG')

    def enumerate(self, type):
        if type in self.enumValues:
            return self.enumValues[type]
        return type

    def executeQuery(self, query):
        if (self.debug):
            print(query)
        with sqlite3.connect('./backend/dummy.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.commit()
            return rows
        return None

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