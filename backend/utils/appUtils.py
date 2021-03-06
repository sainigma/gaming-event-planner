import os, time, datetime
from dotenv import load_dotenv

def init():
    # for running on venv
    if (os.path.basename(os.getcwd()) == 'backend'):
        os.chdir('./..')

    load_dotenv()

    os.environ['TZ'] = 'Europe/Helsinki'
    time.tzset()

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