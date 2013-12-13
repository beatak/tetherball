#! /usr/bin/env python

import argparse, os.path, os, sys, time
from notifier import Notifier
from fsevents import Observer, Stream
from config import Config
import daemon

def run_process (path, name):
    # daemonize
    pid = daemon.createDaemon()

    # since, it's daemon, you can't do print
    n = Notifier( title='Tetherball' )

    # spit pid
    try:
        file_pid = open( os.path.join( Config.PATH_TETHERBALL_PROC, name ), 'w' )
        file_pid.write( str(pid) )
        file_pid.close()
    except Exception, e:
        n.message( message=("Failed to write pid into file: %s" % e) )

    # debug message
    # n.message( message=("%s: %s" % (name, str( pid ))) )

    def callback(FileEvent):
        # mask, cookie, name
        n.message( message=("mask: %s, cookie: %s\npath: %s" % (FileEvent.mask, FileEvent.cookie, FileEvent.name)) )

    observer = Observer()
    observer.start()
    stream = Stream(callback, path, file_events=True)
    observer.schedule(stream)

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='Run Tetherball file change watcher' )
    parser.add_argument( 'path', type=str, nargs=1, help='Tetherball will watch this path' )
    parser.add_argument( '--name', type=str, help='You can set the name for the path' )
    args = parser.parse_args()
    path = args.path[0]
    if not os.path.exists( path ):
        print "The given path doesn't seem to exist: %s" % path
        exit( 1 )
    if args.name == None:
        name = str( int(time.time()) )
    else:
        name = args.name

    run_process( path, name )

