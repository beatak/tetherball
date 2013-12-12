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

    def queue (self, list_object, force_standby=False):
        # if dispatcher is running, it'll push to standby
        print 'queue'

    def requeue (self):
        # pull all from standby and push it back to queue
        print 'requeue'

    def dequeue (self):
        # lock the db, read all from queues, if it goes right, call _move_queues, unlock the db
        print 'pop'

    def _move_queues (self):
        # claer queues and move all from standbys to queue
        print 'move'


if __name__ == "__main__":
    from config import Config

    # from config_serializer import ConfigSerializer
    # print json.dumps( Config, cls=ConfigSerializer )

    d = Data( config=Config )

