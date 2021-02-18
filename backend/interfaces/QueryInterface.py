import os

class QueryInterface:
    def __init__(self, enumerate, executeQuery):
        self.enumerate = enumerate
        self.executeQuery = executeQuery
        self.initialize()

        self.usesPSQL = False
        self.usesSQLITE = False
        if (os.getenv('SQL')):
            if (os.getenv('SQL') == 'psql'):
                self.usesPSQL = True
            elif (os.getenv('SQL') == 'sqlite'):
                self.usesSQLITE = True
        
    def initialize(self):
        pass