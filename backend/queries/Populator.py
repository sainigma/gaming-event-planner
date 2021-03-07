import json, os

#Debuggaukseen
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

    def loadStructure(self):
        self.structure = self.loadJson('database/structure.json')
        if (self.structure == None):
            return None

        for table in self.structure['tables'].keys():
                self.createTable(table)
        
        return True

    def populate(self):
        if (os.getenv('DEBUG') and os.getenv('DEBUG') == '1'):
            print('populoin')
            
            self.dummy = self.loadJson('database/dummy.json')

            if (not self.loadStructure() or self.dummy == None):
                return None

            for table in self.dummy.keys():
                if (table in self.actions):
                    for entry in self.dummy[table]:
                        self.actions[table](entry)
        else:
            if (os.getenv('SQL') and os.getenv('SQL') == 'sqlite'):
                self.loadStructure()

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