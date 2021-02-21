import sqlite3, os
from gateways.AbstractGateway import AbstractGateway

# Debuggakseen tarkoitettu gateway
class SQLiteGateway(AbstractGateway):

    def initialize(self):
        self.databaseURI = './backend/dummy.db'

        self.enumValues = {
            'uuid':'integer',
            'int':'integer',
            'timestamp':'integer'
        }
        self.debug = False
        if (os.getenv('DEBUG') and os.getenv('DEBUG') == '1'):
            self.debug = True
        
    def enumerate(self, type):
        if type in self.enumValues:
            return self.enumValues[type]
        return type

    def executeQuery(self, query):
        if (self.debug):
            print(query)
        with sqlite3.connect(self.databaseURI) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.commit()
            return rows
        return None