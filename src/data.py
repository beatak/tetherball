import json, sqlite3
from config import Config

class Data ():
    def __init__ (self, config={}):
        self.conn = sqlite3.connect(config.PATH_TETHERBALL_DB)

        cursor = self.conn.cursor()
        
        self.queue = None
        self.standby = None
        print 'yay'

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
    from debug_json import MyEncoder
    print json.dumps( Config, cls=MyEncoder )

    d = Data( config=Config )

