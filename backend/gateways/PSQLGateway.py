import psycopg2, os
from gateways.AbstractGateway import AbstractGateway

class PSQLGateway(AbstractGateway):

    def initialize(self):
        self.uri = os.getenv('DATABASE_URL')
        self.debug = False
        if (os.getenv('DEBUG') and os.getenv('DEBUG') == '1'):
            self.debug = True

    #todo: connection poolaus
    def executeQuery(self, query):
        if (self.debug):
            print(query)

        with psycopg2.connect(self.uri) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                try:
                    rows = cursor.fetchall()
                    print(cursor.statusmessage)
                except psycopg2.ProgrammingError:
                    # poikkeus on tilanteita varten jossa insert palauttaa arvon
                    rows = []
        return rows