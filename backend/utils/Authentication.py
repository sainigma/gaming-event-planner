import hashlib, uuid, time, jwt, os

class Authentication:
    def __init__(self):
        self.secret = os.getenv("SECRET")

    def hash(self, target):
        salt = uuid.uuid4().hex
        return self.hashWithSalt(target, salt)
    
    def hashWithSalt(self, target, salt):
        return hashlib.sha256(salt.encode() + target.encode()).hexdigest() + ':' + salt

    def createToken(self, username):
        expires = int(time.time() + 3600 * 24 * 30)
        payload = {"username":username, "expires":expires}
        token = jwt.encode(payload, self.secret, algorithm="HS256")
        return (token, expires)