import os
from interfaces.QueryInterface import QueryInterface
from controllers.GameDBController import GameDBController

class Game(QueryInterface):
    def initialize(self):
        self.gameDB = GameDBController()
        pass

    def getGame(self, gameId):
        query = "select id, name, slug, cover from games where id = {0}".format(int(gameId))
        result = self.executeQuery(query)
        if (len(result) > 0):
            result = result[0]
            return {
                "id":int(result[0]),
                "name":result[1],
                "slug":result[2],
                "cover":result[3],
                "cache":1
            }
        game = self.gameDB.getGame(gameId)
        game['name'] = game.get('name').replace("'", "").replace('"', "")
        insertGame = "insert into games (id, name, slug, cover) values ({0}, '{1}', '{2}', '{3}')".format(int(game.get('id')), str(game.get('name')), str(game.get('slug')), str(game.get('cover')))
        self.executeQuery(insertGame)
        return(game)

    def findGames(self, name):
        return self.gameDB.findGames(name)