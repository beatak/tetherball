#! /usr/bin/env python

import argparse, os.path, os, sys, time
from fsevents import Observer, Stream # pypy

import daemon
from config import Config
from data import Data
from notifier import Notifier
from logger import Logger

import json

def run_process (path, repository):
    # daemonize
    pid = daemon.createDaemon()

    # since, it's daemon, you can't do print
    n = Notifier( title='Tetherball' )
    d = Data( config=Config )

    # spit pid
    try:
        file_pid = open( os.path.join( Config.PATH_TETHERBALL_PROC, repository ), 'w' )
        file_pid.write( str(pid) )
        file_pid.close()
    except Exception, e:
        n.message( message=("Failed to write pid into file: %s" % e) )

    # debug message
    # n.message( message=("%s: %s" % (repository, str( pid ))) )

    # FileEvent: mask, cookie, name
    def callback(FileEvent):
        l = Logger(Config)        
        timestamp = int(time.time())
        n.message( message=("time: %i, repo: %s, path: %s, mask: %s, cookie: %s" % (timestamp, repository, FileEvent.name, FileEvent.mask, FileEvent.cookie)) )

        try:
            len_path_prefix = len( Config.repository[ repository ]['local'] )
            relative_path = FileEvent.name[len_path_prefix:]

            arr = os.path.split( relative_path )
            if arr 


            l.debug( "%s / %s (%s)" % (repository, relative_path, json.dumps(Config.repository[repository]) ) )



            d.queue( timestamp, [{'repository': repository, 'path': FileEvent.name }] )

        except Exception, e:
            n.message( message=("Error on FileEvent callback: %s" % e) )
            l.debug( "Error on FileEvent callback: %s" % e )

    observer = Observer()
    observer.start()
    stream = Stream(callback, path, file_events=True)
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
