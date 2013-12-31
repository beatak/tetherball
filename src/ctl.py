#!/usr/bin/env python

import os.path, argparse, subprocess, json
import psutil #pip

from config import Config
import daemon
from data import Data
from logger import Logger

KNOWN_COMMAND = ('start', 'stop', 'restart', 'status', 'refresh_db', 'show_queues', 'show_config', 'help', 'rotate_log')
path_origin = os.path.dirname( os.path.abspath( __file__ ) )


def run_command (command, args):
    # fixme: probably I should remove LOCK || not used anymore
    if command == 'start':
        command_start()
    elif command == 'stop':
        command_stop(args)
    elif command == 'restart':
        command_stop()
        command_start()
    elif command == 'status':
        command_status()
    elif command == 'refresh_db':
        command_refresh_db()
    elif command == 'show_queues':
        command_show_queues()
    elif command == 'show_config':
        command_show_config()
    elif command == 'help':
        command_help()
    elif command == 'rotate_log':
        command_rotate_log()
    exit( 0 )

def command_help ():
    print "ctl.py accepts:"
    mylist = list((KNOWN_COMMAND[:]))
    mylist.sort()
    for command in mylist:
        print " * " + command

def command_start ():
    for name in Config.repository:
        path_exec = os.path.join( path_origin, 'watcher.py' )
        path_local = str( Config.repository[name]['local'] )
        try:
            # this strcuture make name without a space...
            subprocess.call(' '.join( [path_exec, path_local, name] ), shell=True)
        except Exception, e:
            print "Failed to spawn a new process: %s" % e

def command_stop (args):
    try:
        procs = os.listdir( Config.PATH_TETHERBALL_PROC )
        for proc in procs:
            path_proc = os.path.join( Config.PATH_TETHERBALL_PROC, proc )
            f = open( path_proc , 'r' )
            pid = int( f.read() )
            f.close()
            psutil.Process( pid ).terminate()
            os.unlink( path_proc )
    except psutil.NoSuchProcess, e:
        if args.force:
            result = []
            try:
                for proc in procs:
                    mypath = os.path.join( Config.PATH_TETHERBALL_PROC, proc )
                    os.unlink( mypath )
                    result.append( ' * ' + mypath )
            except Exception, e:
                print "Failed to delete lockfiles: %s" % e
                print "You might need to clean up %s directory manually" % Config.PATH_TETHERBALL_PROC
                exit( 1 )
            print "Removed files:"
            print "\n".join( result )
        else:
            print "Failed to stop daemons: %s" % e
            print "Try --force to remove lockfiles."
        exit( 1 )
    except psutil.AccessDenied, e:
        print "Failed to stop daemons: %s" % e
        print "You might need to do sudo."
        exit( 1 )
    except Exception, e:
        print "Failed to stop daemons: %s" % e
        exit( 1 )

def command_status ():
    try:
        procs = os.listdir( Config.PATH_TETHERBALL_PROC )
        if len( procs ) > 0:
            result = []
            for proc in procs:
                path_proc = os.path.join( Config.PATH_TETHERBALL_PROC, proc )
                f = open( path_proc , 'r' )
                pid = str( int( f.read() ) )
                f.close()
                result.append( "%s is running as %s." % (proc, pid) )
            print ' / '.join( result )
        else:
            print 'Tetherball is not running.'
    except Exception, e:
        print "Failed to run status: %s" % e
        exit( 1 )

def command_refresh_db ():
    try:
        d = Data(Config)
        d.drop_table(True, True)
        d.init_table()
    except Exception, e:
        print "Failed to run refresh db: %s" % e
        exit( 1 )

def command_show_queues ():
    try:
        d = Data(Config)
        result = d.fetch_queues()
        print json.dumps(result, indent=2)
    except Exception, e:
        print "Failed to run refresh db: %s" % e
        exit( 1 )

def command_rotate_log ():
    try:
        os.unlink( Config.PATH_TETHERBALL_LOGGER )
        open( Config.PATH_TETHERBALL_LOGGER, 'a' ).close()
        pass
    except Exception, e:
        print "Failed to rotate log: %s" % e
        exit( 1 )

def command_show_config ():
    from config_serializer import ConfigSerializer
    print json.dumps( Config, cls=ConfigSerializer, indent=2, sort_keys=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description='Manage Tetherball application' )
    parser.add_argument( 'command', type=str, nargs=1, help='start/stop/restart watching Tetherball' )
    parser.add_argument( '--force', action='store_true', help='when you do `stop --force`, Tetherball will delete lockfiles no matter what.'  )
    args = parser.parse_args()

    if args.command[0] in KNOWN_COMMAND:
        run_command(args.command[0], args)
    else:
        print "Unknow command: %s" % args.command[0]
        parser.print_help()
        exit( 1 )

