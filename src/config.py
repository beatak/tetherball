import os.path
import json

class Config:
    pass

Config.FILE_BASE     = '.tetherball'
Config.FILE_LOCKFILE = 'lockfile'
Config.FILE_DB       = 'sqlite.db'
Config.PATH_CWD = os.path.expanduser('~')
Config.PATH_TETHERBALL_BASE = os.path.join( Config.PATH_CWD,             Config.FILE_BASE )
Config.PATH_TETHERBALL_LOCK = os.path.join( Config.PATH_TETHERBALL_BASE, Config.FILE_LOCKFILE )
Config.PATH_TETHERBALL_DB   = os.path.join( Config.PATH_TETHERBALL_BASE, Config.FILE_DB )

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

if __name__ == "__main__":
    from config_serializer import ConfigSerializer
    print json.dumps( Config, cls=ConfigSerializer )

