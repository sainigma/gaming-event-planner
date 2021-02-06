import os, json, requests, time
from igdb.wrapper import IGDBWrapper
from igdb.igdbapi_pb2 import GameResult

class GameDBController():
    def __init__(self):
        self.id = os.getenv("IGDBID")
        self.key = os.getenv("IGDBKEY")
        self.token = os.getenv("IGDBTOKEN")
        self.timeout = int(os.getenv("IGDBTIMEOUT"))
        self.active = False

        if (self.token != None):
            self.wrapper = IGDBWrapper(self.id, self.token)
            self.active = True
            #self.getGame(355)
            #self.findGames("Quake III Arena")
        else:
            self.token = self.getAccessToken()
            if (self.token == None):
                print("IGDB Connection failed")
    
    def ok(self):
        if (not self.active):
            return False
        return self.testTimeout()

    def testTimeout(self):
        if (time.time() > self.timeout):
            self.getAccessToken()
            if (self.token == None):
                return False
        return True

    def getGame(self, gameid):
        if (self.ok()):
            req = ['games', 'fields slug, name; where id = 355;']
            result = self.dump(req)
            return result
        return None

    def findGames(self, name):
        if (self.ok()):
            req = ['games', 'fields id, slug, name; search "' + name + '";']
            result = self.dump(req)
            print(result)
            return result
        return None

    def getAccessToken(self):
        print("renewing..")
        uri = "https://id.twitch.tv/oauth2/token?client_id="+self.id+"&client_secret="+self.key+"&grant_type=client_credentials"
        result = requests.post(uri).json()
        if ("access_token" in result):
            self.timeout = int(time.time() + result["expires_in"])
            print("token: ", result["access_token"], " timeout: ", self.timeout)
            return result["access_token"]
        return None

    def dump(self, req):
        target = req[0]
        request = req[1]

        byteArr = self.wrapper.api_request(target, request)
        res = byteArr.decode('utf8').replace("'", '"')
        data = json.loads(res)
        return data