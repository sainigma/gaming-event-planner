import os, time, datetime
from dotenv import load_dotenv
from gateways.SQLiteGateway import SQLiteGateway
from gateways.PSQLGateway import PSQLGateway

def init():
    if (os.path.basename(os.getcwd()) == 'backend'):
        # for running on venv
        os.chdir('./..')

    load_dotenv()

    os.environ['TZ'] = 'Europe/Helsinki'
    time.tzset()

def initGateway():
    selector = os.getenv('SQL')
    gateway = None
    if (selector == 'sqlite'):
        gateway = SQLiteGateway()
    elif (selector == 'psql'):
        gateway = PSQLGateway()
    return gateway

def createDate(dateString):
    try:
        eTime = int(time.mktime(datetime.datetime.strptime(dateString, "%Y-%m-%d").timetuple()))
        return eTime
    except ValueError:
        return None

def containsEvil(content):
    # muista tehdä kunnon tarkistus
    if ';' in str(content):
        return True
    return False

def sanitize(params):
    for item in params:
        if (item == None or containsEvil(item)):
            return False
    return True

def getUsernameFromVerification(req, gateway):
    bearer = req.headers.get('Authorization')
    if (bearer == None):
        return None
    return gateway.verify(bearer)