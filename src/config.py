import os.path
import json
from config_serializer import ConfigSerializer

class Config:
    @staticmethod
    def store ():
        result = {}
        try:
            for _key in Config.__dict__.keys():
                _obj = Config.__dict__[_key]
                if _key.startswith('__'):
                    # print 'special attributes'
                    continue
                elif _obj == None:
                    # print 'None'
                    continue
                elif hasattr(_obj, '__func__') or hasattr(_obj, '__call__'):
                    # print 'function'
                    continue
                else:
                    result[_key] = _obj
        except Exception, e:
            print "Something went wrong at storing config: %s" % str( e )
            exit(1)

        f = open( Config.PATH_TETHERBALL_CONFIG, 'w')
        f.write( json.dumps(result, indent=2) )
        f.close()

    @staticmethod
    def add_repository (name='', remote=''):
        if name == '' or remote == '':
            raise Exception('name and remote argument are both needed')
        Config.repository[ name ] = { 'remote': remote }

Config.FILE_BASE    = '.tetherball'
Config.FILE_COMMIT  = 'commit.lock'
Config.FILE_PUSH    = 'push.lock'
Config.FILE_CONFIG  = 'config.json'
Config.FILE_DB      = 'sqlite.db'
Config.FILE_PROC    = 'proc'
Config.FILE_LOGGER  = 'tetherball.log'
Config.FILE_QUEUE   = 'queue'
Config.PATH_USERDIR = os.path.expanduser('~')

Config.PATH_TETHERBALL_BASE    = os.path.join( Config.PATH_USERDIR,         Config.FILE_BASE     )
Config.PATH_TETHERBALL_COMMIT  = os.path.join( Config.PATH_TETHERBALL_BASE, Config.FILE_COMMIT   )
Config.PATH_TETHERBALL_PUSH    = os.path.join( Config.PATH_TETHERBALL_BASE, Config.FILE_PUSH     )
Config.PATH_TETHERBALL_CONFIG  = os.path.join( Config.PATH_TETHERBALL_BASE, Config.FILE_CONFIG   )
Config.PATH_TETHERBALL_DB      = os.path.join( Config.PATH_TETHERBALL_BASE, Config.FILE_DB       )
Config.PATH_TETHERBALL_PROC    = os.path.join( Config.PATH_TETHERBALL_BASE, Config.FILE_PROC     )
Config.PATH_TETHERBALL_LOGGER  = os.path.join( Config.PATH_TETHERBALL_BASE, Config.FILE_LOGGER   )
Config.PATH_TETHERBALL_QUEUE   = os.path.join( Config.PATH_TETHERBALL_BASE, Config.FILE_QUEUE    )

if os.path.exists( Config.PATH_TETHERBALL_BASE ):
    if not os.path.isdir( Config.PATH_TETHERBALL_BASE ):
        print "%s is not a directory? You may need to fix is manually" % Config.PATH_TETHERBALL_BASE
        exit( 1 )
else:
    os.mkdir( Config.PATH_TETHERBALL_BASE )

if os.path.exists( Config.PATH_TETHERBALL_PROC ):
    if not os.path.isdir( Config.PATH_TETHERBALL_PROC ):
        print "%s is not a directory? You may need to fix is manually" % Config.PATH_TETHERBALL_PROC
        exit( 1 )
else:
    os.mkdir( Config.PATH_TETHERBALL_PROC )

if os.path.exists( Config.PATH_TETHERBALL_QUEUE ):
    if not os.path.isdir( Config.PATH_TETHERBALL_QUEUE ):
        print "%s is not a directory? You may need to fix is manually" % Config.PATH_TETHERBALL_QUEUE
        exit( 1 )
else:
    os.mkdir( Config.PATH_TETHERBALL_QUEUE )

Config.repository = {}
Config.lock = False

# update config by saved thing
if os.path.exists( Config.PATH_TETHERBALL_CONFIG ):
    f = open( Config.PATH_TETHERBALL_CONFIG, 'r' )
    try:
        d = json.loads( f.read() )
        f.close()
    except Exception, e:
        print "Failed to load config.json: %s" % str( e )
        exit( 1 )
    for k in d:
        Config.__dict__[k] = d[k]

if __name__ == "__main__":
    print "DEBUGING: " + json.dumps( Config, cls=ConfigSerializer, indent=2 )
    try:
        Config.foobar = Config.foobar + 1
    except:
        Config.foobar = 0
    # Config.add_repository(name='tetherball', remote='git://tmizohata.vm.ny4dev.etsy.com/home/tmizohata/development/tetherball')
    Config.store()

