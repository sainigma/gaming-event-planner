from interfaces.QueryInterface import QueryInterface
class Group(QueryInterface):

    def getGroupId(self, groupname):
        query = "select id from usergroups where name = '{0}'".format(str(groupname))
        result = self.executeQuery(query)
        if (len(result) > 0):
            return result[0][0]
        return False

    def isOwner(self, userId, groupId):
        query = 'select 1 from usergroupregister where userid = {0} and usergroup = {1} and rights = 2'.format(int(userId), int(groupId))
        result = self.executeQuery(query)
        if (len(result) > 0):
            return True
        return False

    def addToGroup(self, userId, targetId, targetgroup):
        groupId = self.getGroupId(targetgroup)
        if (groupId == False):
            return False
        if (not self.isOwner(userId, groupId)):
            return False
        
        query = 'update usergroupregister set accepted = True, inviter = {0} where usergroup = {1} and userid = {2}'.format(int(userId), int(groupId), int(targetId))
        self.executeQuery(query)
        return True

    def createGroup(self, userId, groupname):
        query = "insert into usergroups (name) values ('{0}')".format(str(groupname))
        if (self.usesPSQL):
            query += ' returning id'
            result = self.executeQuery(query)
        else:
            self.executeQuery(query)
            result = self.executeQuery('select max(id) from usergroups')
        
        groupId = result[0][0]
        query = "insert into usergroupregister (userid, inviter, usergroup, rights, verified, accepted) values ({0}, {0}, {1}, 2, TRUE, TRUE)".format(int(userId), int(groupId))
        self.executeQuery(query)
        pass

    def getRequests(self, userId):
        subquery = 'select usergroup from usergroupregister where userid = {0} and rights = 2'.format(int(userId))
        query = 'select u.username, g.name from usergroupregister left join users u on u.id = userid left join usergroups g on usergroup = g.id where usergroup in ({0}) and accepted = FALSE'.format(str(subquery))
        return self.executeQuery(query)

    def getParticipatingGroups(self, userId):
        query = 'select usergroup, u.name from usergroupregister left join usergroups u on usergroup = u.id where userid = {0} and verified = TRUE and accepted = TRUE and rights != 2'.format(int(userId))
        return self.executeQuery(query)

    def getOwnedGroups(self, userId):
        query = 'select usergroup, u.name from usergroupregister left join usergroups u on usergroup = u.id where userid = {0} and rights = 2'.format(int(userId))
        return self.executeQuery(query)

    def joinGroup(self, userId, groupname):
        groupId = self.getGroupId(groupname)
        if (groupId == False):
            self.createGroup(userId, groupname)
            return True
        else:
            query = "insert into usergroupregister (userid, usergroup, rights, verified, accepted) values ({0}, {1}, 0, TRUE, FALSE)".format(int(userId), int(groupId))
            self.executeQuery(query)
        return False
