#! /usr/bin/env python

import argparse, os.path, os, sys, time
import sh
from config import Config
from data import Data

#debug
from logger import Logger
from notifier import Notifier
import json

def run (repository):
    print repository

    ##
    # - maybe timeout?

    # - find if there's a lock file -- if there is, stop
    # if os.path.exists( Config.PATH_TETHERBALL_PUSHER ):
    #     print "locked!"
    #     exit( 1 )

    # - create a lock file
    file_lock = open( Config.PATH_TETHERBALL_PUSHER, 'w' )
    file_lock.write( str( os.getpid() ) )
    file_lock.close()

    # - take all queue
    d = Data( config=Config )
    queues = d.fetch_queues()
    # print json.dumps( queues, indent=2 )

    #   - check if that exists, and if it does: add, if not: rm
    prefix_path = Config.repository[repository]['local']
    action_add = []
    action_rm = []
    for item in queues:
        relative_path = str( item[2] )
        if os.path.exists( os.path.join(prefix_path, relative_path) ):
            action_add.append( relative_path )
        else:
            action_rm.append( relative_path )
    print action_add
    print action_rm

    # - git push
    git = sh.git.bake(_cwd=prefix_path)
    try:
        if len(action_add) > 0:
            git.add( ' '.join(action_add) )
        if len(action_rm) > 0:
            git.rm( ' '.join(action_rm) )
        if len(action_add) > 0 or len(action_rm) > 0:
            _t = int( time.time() )
            git.commit( '-m tetherball %d' % _t )
            git.push()
    except Exception, e:
        print "Failed to operate git: %s" % e
        exit( 1 )

    # - run notifier
    # - delete lock file
    # - check if there's standbys

    exit( 0 )


if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='Run Tetherball git pusher' )
    parser.add_argument( 'repository', type=str, help='Name of the repository registered to Tetherball' )

    args = parser.parse_args()
    # print( dir( Config.repository ) )
    # print Config.repository.keys
    if not args.repository in Config.repository.iterkeys():
        print "`%s` doesn't seem to be registered to Tetherball." % args.repository
        exit( 1 )
    run( args.repository )
