import psycopg2


class connection:
    def __init__(self, dbname, host, user, password, port):
        self.dbname = dbname
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def __del__(self):
        self.disconnect()

    def connect(self):
        if self.connection is psycopg2.connect:
            raise RuntimeError("already connected")
        try:
            #"dbname='geosense_ga' user='gisa_dev' password='t.swlres5r' host='10.110.1.13'"
            conn_str = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (self.dbname, self.user, self.host, self.password, self.port)
            self.connection = psycopg2.connect(conn_str)
            self.connection.set_client_encoding('UTF-8')
        except:
            raise RuntimeError("I am unable to connect to '%s' database" % (self.dbname))
        return()

    def disconnect(self):
        if self.connection is psycopg2.connect:
            self.connection.close()
        return()

class model(object):
    """docstring for model"""
    def __init__(self, arg):
        super(model, self).__init__()
        self.arg = arg



        
