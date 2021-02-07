import json
class Populator:
    def __init__(self, parent):
        self.enumerate = parent.enumerate
        self.executeQuery = parent.executeQuery
        self.parent = parent
        self.actions = {
            'users':self.newUser
        }

    def loadStructure(self):
        with open('database/structure.json') as structure:
            return json.load(structure)

    def loadDummy(self):
        with open('database/dummy.json') as dummy:
            return json.load(dummy)

    def newUser(self, entry):
        username = entry['username']
        password = entry['password']
        self.parent.newUser(username, password)

    def populate(self):
        self.structure = self.loadStructure()
        self.dummy = self.loadDummy()
        
        for table in self.structure['tables'].keys():
            self.createTable(table)
        for table in self.dummy.keys():
            if (table in self.actions):
                for entry in self.dummy[table]:
                    self.actions[table](entry)

    def createTable(self, key):
        table = self.structure['tables'][key]
        idtype = 'id ' + self.enumerate(table['id']) + ' primary key' if 'id' in table else 'id ' + self.enumerate('int') + ' primary key'
        query = 'create table ' + key + ' ( ' + idtype
        for field in table.keys():
            if (field != "id"):
                fiedltType = self.enumerate(table[field])
                query += ', ' + field + ' ' + fiedltType
        query += ' );'
        self.executeQuery(query)