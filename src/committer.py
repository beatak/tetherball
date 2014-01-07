#! /usr/bin/env python

import argparse, os.path, os, sys, time, subprocess, shutil
import sh # pip

from config import Config
from data import Data

#debug
from logger import Logger
from notifier import Notifier
import json

NOTIFIER_TITLE='Tetherball:Committer'
SEC_SLEEP = 1.0
COMMAND = 'ls -t %s | head -1' % Config.PATH_TETHERBALL_QUEUE


def run (repository):
    n = Notifier( title=NOTIFIER_TITLE )
    n.message( message=( "committer::run( '%s' )" % repository ) )

    # - create a lock file
    file_lock = open( Config.PATH_TETHERBALL_COMMIT, 'w' )
    file_lock.write( str( os.getpid() ) )
    file_lock.close()

    # timeout
    time.sleep( SEC_SLEEP )
    try:
        str_last = subprocess.check_output( COMMAND, shell=True )
        ms_now = int( time.time() * 1000 )

        if str_last != '':
            ms_last = int( str_last.strip() )
        else:
            ms_last = ms_now - int(SEC_SLEEP * 1000) - 1

        if (ms_now - ms_last) > (SEC_SLEEP * 1000):
            _run_main(repository)
        else:
            run(repository)
    except Exception, e:
        l = Logger(Config)
        l.debug( 'Failed on committer.py: %s' % e)

def _run_main (repository):
    # - take all queue
    d = Data( config=Config )
    queues = d.fetch_queues()
    # print json.dumps( queues, indent=2 )
    d.drop_table(True)
    d.init_table()

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
    # print action_add
    # print action_rm

    # - git commit
    git = sh.git.bake(_cwd=prefix_path)
    try:
        if len(action_add) > 0:
            git.add( *action_add )
        if len(action_rm) > 0:
            git.rm( *action_rm )
        if len(action_add) > 0 or len(action_rm) > 0:
            _t = int( time.time() )
            git.commit( '-m tetherball %d' % _t )
            # git.push()
    except Exception, e:
        print "Failed to operate git: %s" % e
        exit( 1 )

    # - run notifier
    n = Notifier( title=NOTIFIER_TITLE )
    n.message( message=("Files added: (%s) removed(%s)" % (", ".join(action_add), ", ".join(action_rm)) ) )

    # - delete lock file
    try:
        # delete all queues
        shutil.rmtree( Config.PATH_TETHERBALL_QUEUE )
        os.mkdir( Config.PATH_TETHERBALL_QUEUE )
        # delete lock file
        os.unlink( Config.PATH_TETHERBALL_COMMIT )
    except Exception, e:
        print( "" )

    # - check if there's standbys
    # FIXME: implement this
    exit( 0 )


if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='Run Tetherball git committer' )
    parser.add_argument( 'repository', type=str, help='Name of the repository registered to Tetherball' )

    args = parser.parse_args()
    # print( dir( Config.repository ) )
    # print Config.repository.keys
    if not args.repository in Config.repository.iterkeys():
        n = Notifier( title=NOTIFIER_TITLE )
        n.message( message=( "`%s` doesn't seem to be registered to Tetherball." % args.repository ) )
        print "`%s` doesn't seem to be registered to Tetherball." % args.repository
        exit( 1 )

    # - find if there's a lock file -- if there is, stop
    if os.path.exists( Config.PATH_TETHERBALL_COMMIT ):
        print( 'Lock file exists. If no committer is running, delete %s maybe?' % Config.PATH_TETHERBALL_COMMIT )
        exit( 1 )
    run( args.repository )

