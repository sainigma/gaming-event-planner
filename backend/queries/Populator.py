import json, os
class Populator:
    def __init__(self, parent):
        self.enumerate = parent.enumerate
        self.executeQuery = parent.executeQuery
        self.parent = parent
        self.actions = {
            'users':self.newUser,
            'userrelations':self.newRelation
        }

    def loadJson(self, filepath):
        fullpath = os.getcwd() + '/backend/' + filepath
        if (os.path.exists(fullpath)):
            with open(fullpath) as jsonfile:
                return json.load(jsonfile)
        else:
            print(filepath + ' not found')
        return None

    def newUser(self, entry):
        username = entry['username']
        password = entry['password']
        self.parent.newUser(username, password)

    def newRelation(self, entry):
        user = entry['user']
        target = entry['target']
        relationType = entry['relationType']
        self.parent.newRelation(user, target, relationType)

    def populate(self):
        print('populoin')
        self.structure = self.loadJson('database/structure.json')
        self.dummy = self.loadJson('database/dummy.json')
        
        if (self.structure == None or self.dummy == None):
            return None

        for table in self.structure['tables'].keys():
            self.createTable(table)
        for table in self.dummy.keys():
            if (table in self.actions):
                for entry in self.dummy[table]:
                    self.actions[table](entry)

    def createTable(self, key):
        table = self.structure['tables'][key]
        idtype = 'id ' + self.enumerate(table['id']) + ' primary key' if 'id' in table else 'id ' + self.enumerate('int') + ' primary key' + ' autoincrement'
        query = 'create table if not exists ' + key + ' ( ' + idtype
        for field in table.keys():
            if (field != "id"):
                fiedltType = self.enumerate(table[field])
                query += ', ' + field + ' ' + fiedltType
        query += ' );'
        self.executeQuery(query)