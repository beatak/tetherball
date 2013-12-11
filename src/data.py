import json, sqlite3

class Data ():
    SQL_ENTRIES = """
      CREATE TABLE IF NOT EXISTS
        %s
        ( 
          timestamp INTEGER, 
          repository_id INTEGER, 
          path TEXT NOT NULL
        );"""

    def __init__ (self, config={}):
        conn = sqlite3.connect(config.PATH_TETHERBALL_DB)
        cursor = conn.cursor()
        cursor.execute( self.SQL_ENTRIES % 'queues' )
        cursor.execute( self.SQL_ENTRIES % 'standbys' )
        self.connection = conn

    def refresh (self):
        #foo
        print 'refresh'

    def push (self, list_object):
        # if dispatcher is running, it'll push to standby
        print 'push'

    def pop (self):
        # whatever
        print 'pop'

    def requeue (self):
        # pull all from standby and push it back to queue
        print 'requeue'

if __name__ == "__main__":
    from config import Config
    from debug_json import MyEncoder

    print json.dumps( Config, cls=MyEncoder )

    d = Data( config=Config )

