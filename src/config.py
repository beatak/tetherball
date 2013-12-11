import os.path
import json
from config_serializer import ConfigSerializer

class Config:
    @staticmethod
    def save ():
        s_orig = json.dumps( Config, cls=ConfigSerializer )
        json_o = json.loads( s_orig )
        deleting = []
        for k in json_o:
            if json_o[k] == None:
                deleting.append(k)
        for d in deleting:
            json_o.pop( d, None )
        s_result = json.dumps( json_o )
        f = open( Config.PATH_TETHERBALL_CONFIG, 'w')
        f.write( s_result )
        f.close()
    pass



Config.FILE_BASE     = '.tetherball'
Config.FILE_LOCKFILE = 'lockfile'
Config.FILE_CONFIG   = 'config.json'
Config.FILE_DB       = 'sqlite.db'
Config.PATH_USERDIR = os.path.expanduser('~')

Config.PATH_TETHERBALL_BASE   = os.path.join( Config.PATH_USERDIR,         Config.FILE_BASE )
Config.PATH_TETHERBALL_LOCK   = os.path.join( Config.PATH_TETHERBALL_BASE, Config.FILE_LOCKFILE )
Config.PATH_TETHERBALL_CONFIG = os.path.join( Config.PATH_TETHERBALL_BASE, Config.FILE_CONFIG )
Config.PATH_TETHERBALL_DB     = os.path.join( Config.PATH_TETHERBALL_BASE, Config.FILE_DB )

if os.path.exists( Config.PATH_TETHERBALL_BASE ):
    if not os.path.isdir( Config.PATH_TETHERBALL_BASE ):
        print "%s is not a directory? You may need to fix is manually" % Config.PATH_TETHERBALL_BASE
        exit( 1 )
else:
    os.mkdir( Config.PATH_TETHERBALL_BASE )

    # SQL_REPOSITORIES = """
    #   CREATE TABLE IF NOT EXISTS
    #     repositories
    #     ( 
    #       id INTEGER PRIMARY KEY AUTOINCREMENT,
    #       name TEXT NOT NULL,
    #       remote TEXT NOT NULL
    #     );"""

# update config by saved thing
if os.path.exists( Config.PATH_TETHERBALL_CONFIG ):
    f = open( Config.PATH_TETHERBALL_CONFIG, 'r' )
    try:
        d = json.loads( f.read() )
        f.close()
    except Exception, e:
        print e
        exit( 1 )
    for k in d:
        Config.__dict__[k] = d[k]

if __name__ == "__main__":
    print json.dumps( Config, cls=ConfigSerializer )
    try:
        Config.foobar = Config.foobar + 1
    except:
        Config.foobar = 0        
    Config.save()

