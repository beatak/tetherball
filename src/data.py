import json, sqlite3
from logger import Logger

class Data ():
    TABLE_QUEUES   = 'queues'
    TABLE_STANDBYS = 'standbys'

    SQL_ENTRIES = """
      CREATE TABLE IF NOT EXISTS
        %s
        ( 
          timestamp INTEGER, 
          repository TEXT NOT NULL, 
          path TEXT NOT NULL
        );"""

    SQL_INSERT_ENTRY = """
      INSERT
        INTO %s
          (timestamp, repository, path)
        VALUES
          (%i, "%s", "%s");"""

    SQL_INSERT_ENTRY_VALUES = """INSERT INTO %s (timestamp, repository, path) VALUES %s;"""
    SQL_DROP_TABLE          = """DROP TABLE %s;"""
    SQL_SELECT_ENTRY        = """SELECT * FROM %s ORDER BY timestamp;"""
    SQL_SELECT_NO_DUPE      = """SELECT * FROM %s GROUP BY repository, path ORDER BY timestamp;"""

    def __init__ (self, config={}):
        self.log = Logger(config)
        self.log.debug( 'Data init()' )
        self.config = config
        self.init_table()

    def init_table (self):
        try:
            connection = sqlite3.connect(self.config.PATH_TETHERBALL_DB)
            cursor = connection.cursor()
            cursor.execute( self.SQL_ENTRIES % self.TABLE_QUEUES )
            cursor.execute( self.SQL_ENTRIES % self.TABLE_STANDBYS )
            connection.commit()
            connection.close()
        except Exception, e:
            self.log.debug( "Failed to issue sql init_table(): %s" % e )

    def drop_table (self, queues=False, standbys=False):
        try:
            connection = sqlite3.connect(self.config.PATH_TETHERBALL_DB)
            cursor = connection.cursor()
            if queues:
                self.log.debug( "Dropping `queues` table" )
                cursor.execute( self.SQL_DROP_TABLE % self.TABLE_QUEUES )
            if standbys:
                self.log.debug( "Dropping `standbys` table" )
                cursor.execute( self.SQL_DROP_TABLE % self.TABLE_STANDBYS )
            connection.commit()
            connection.close()
        except Exception, e:
            self.log.debug( "Failed to issue sql on drop_table(): %s" % e )

    def queue (self, timestamp, list, force_standby=False):
        # if dispatcher is running, it'll push to standby
        len_list = len( list )
        if force_standby:
            repo = self.TABLE_STANDBYS
        else:
            repo = self.TABLE_QUEUES

        sql =''
        try:
            # n.message( message=('LEN: %i' % len_list) )
            if len_list == 0:
                raise Exception('list argument needs to contain at least one value.')
            elif len_list == 1:
                sql = self.SQL_INSERT_ENTRY % (repo, timestamp, list[0]['repository'], list[0]['path'])
            else:
                partial = []
                for row in list:
                    partial.append( ''.join(['( ', timestamp, ', "', row['repository'], '" ,', row['path'], '" )']) )
                sql = self.SQL_INSERT_ENTRY_VALUES % (repo, ','.join(partial))
        except Exception, e:
            self.log.debug( 'DATA: %s' % e )
            exit( 1 )

        self.log.debug( 'SQL: %s' % sql )

        try:
            connection = sqlite3.connect(self.config.PATH_TETHERBALL_DB)
            cursor = connection.cursor()
            cursor.execute( sql )
            connection.commit()
            connection.close()
        except Exception, e:
            self.log.debug( "Failed to issue sql on queue(): %s" % e )

    def requeue (self):
        # pull all from standby and push it back to queue
        print 'requeue lala'

    def dequeue (self):
        # lock the db, read all from queues, if it goes right, call _move_queues, unlock the db
        print 'pop'

    def fetch_queues(self):
        result = None
        try:
            connection = sqlite3.connect(self.config.PATH_TETHERBALL_DB)
            cursor = connection.cursor()
            cursor.execute( self.SQL_SELECT_NO_DUPE % self.TABLE_QUEUES )
            result = cursor.fetchall()
            connection.commit()
            connection.close()
        except Exception, e:
            self.log.debug( "Failed to issue sql on fetch_queues(): %s" % e )
        return result

    def _move_queues (self):
        # claer queues and move all from standbys to queue
        print 'move'

    def _show_values (self):
        result = []
        try:
            connection = sqlite3.connect(self.config.PATH_TETHERBALL_DB)
            cursor = connection.cursor()
            cursor.execute( self.SQL_SELECT_ENTRY % self.TABLE_QUEUES )
            result.append( cursor.fetchall() )
            cursor.execute( self.SQL_SELECT_ENTRY % self.TABLE_STANDBYS )
            result.append( cursor.fetchall() )
            connection.commit()
            connection.close()
        except Exception, e:
            self.log.debug( "Failed to issue sql on show_values(): %s" % e )
        return result

if __name__ == "__main__":
    from config import Config

    # from config_serializer import ConfigSerializer
    # print json.dumps( Config, cls=ConfigSerializer )

    d = Data( config=Config )
    result = d._show_values()
    print json.dumps(result, indent=2)

