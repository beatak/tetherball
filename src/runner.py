#! /usr/bin/env python

import argparse, os.path, os, sys, time
from fsevents import Observer, Stream # pypy
from config import Config

#debug
from logger import Logger
from notifier import Notifier
import json

def run_process (path, repository):
    #imports
    import daemon

    # daemonize
    pid = daemon.createDaemon()

    # spit pid
    try:
        file_pid = open( os.path.join( Config.PATH_TETHERBALL_PROC, repository ), 'w' )
        file_pid.write( str(pid) )
        file_pid.close()
    except Exception, e:
        # l = Logger(Config)
        # l.debug( "Failed to write pid into file: %s" )
        n = Notifier( title='Tetherball' )
        n.message( message=("Failed to write pid into file: %s" % e) )

    # debug message
    # n.message( message=("%s: %s" % (repository, str( pid ))) )

    _run_observer( path, repository )


def _run_observer (path, repository):
    #imports
    import re, fnmatch # TODO? windows version for this??
    from data import Data

    # FileEvent: mask, cookie, name
    def _callback(FileEvent):
        try:
            timestamp = int(time.time())
            d = Data( config=Config )
            len_path_prefix = len( Config.repository[ repository ]['local'] )
            relative_path = FileEvent.name[len_path_prefix:]
            arr_relative_path = os.path.split( relative_path )
            ignores = Config.repository[ repository ]['ignore']
            is_matched = False

            #debug
            l = Logger(Config)
            n = Notifier( title='Tetherball' )
            n.message( message=("time: %i, repo: %s, path: %s, mask: %s, cookie: %s" % (timestamp, repository, FileEvent.name, FileEvent.mask, FileEvent.cookie)) )
            l.debug( "FSEvent: repository(%s), relative_path(%s), config(%s)" % (repository, relative_path, json.dumps(Config.repository[repository]) ) )

            # FIXME: this won't support * dir name...!
            for ignore in ignores:
                arr_ignore_path = os.path.split( ignore )
                if len( arr_ignore_path ) > 1:
                    basedir_ignore_path = os.path.join( arr_ignore_path[0:-1] )

                    if len( arr_relative_path ) > 1:
                        # - ignore includes '/' and event path includes '/'
                        basedir_relative_path = os.path.join( arr_relative_path[0:-1] )
                        if relative_path.startswith( basedir_ignore_path ):
                            regex_matcher = re.compile( fnmatch.translate(arr_ignore_path[-1]) )
                            regex_matchee = arr_relative_path[-1]

                    else:
                        # - ignore includes '/' and event path doesn't include '/'
                        regex_matcher = regex_matchee = None
 
                else:
                    if len( arr_relative_path ) > 1:
                        # - ignore doesn't include '/' and event path includes '/'
                        regex_matcher = re.compile( fnmatch.translate(ignore) )
                        regex_matchee = arr_relative_path[-1]

                    else:
                        # - ignore doesn't include '/' and event path doesn't include '/'
                        regex_matcher = re.compile( fnmatch.translate(ignore) )
                        regex_matchee = relative_path

                if (regex_matcher and regex_matchee) and regex_matcher.match( regex_matchee ):
                    is_matched = True
                    # l.debug( " ** %s matched to %s" % (relative_path, ignore) )
                    continue

            if is_matched:
                l.debug( "IGNORED: %s" % relative_path )
            else:
                l.debug( "REGISTERED: %s" % relative_path )
                d.queue( timestamp, [{'repository': repository, 'path': relative_path }] )

        except Exception, e:
            n.message( message=("Error on FileEvent callback: %s" % e) )
            l.debug( "Error on FileEvent callback: %s" % e )

    observer = Observer()
    observer.start()
    stream = Stream(_callback, path, file_events=True)
    observer.schedule(stream)


if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='Run Tetherball file change watcher' )
    parser.add_argument( 'path', type=str, help='Tetherball will watch this path' )
    parser.add_argument( 'repository', type=str, help='Name of the repository registered to Tetherball' )

    args = parser.parse_args()
    path = args.path
    if not os.path.exists( path ):
        print "The given path doesn't seem to exist: %s" % path
        exit( 1 )
    repository = args.repository

    run_process( path, repository )
