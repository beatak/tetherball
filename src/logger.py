import logging

class Logger():
    def __init__ (self, config):
        try:
            logging.basicConfig( filename=config.PATH_TETHERBALL_LOGGER, level=logging.DEBUG )
        except Exception, e:
            print "Failed to start Log, probably not passing config?: %s" % e
            exit( 1 )

    def debug (self, msg):
        logging.debug( msg )

if __name__ == "__main__":
    from config import Config
    log = Logger(Config)
    log.debug( 'HEY BABY' )

