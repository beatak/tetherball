#! /usr/bin/env python

# `git symbolic-ref HEAD --short` requires newer version of git

import argparse, os.path, subprocess
import sh #pip
import spur #pip

from config import Config
from data import Data

#debug
from logger import Logger
from notifier import Notifier

NOTIFIER_TITLE='Tetherball:PushMerge'
path_origin = os.path.dirname( os.path.abspath( __file__ ) )
if os.path.islink( __file__ ):
    path_origin = os.path.dirname( os.path.abspath( os.path.realpath( __file__ ) ) )


def log_error (msg):
    n = Notifier( title=NOTIFIER_TITLE )
    n.message( message=( msg ) )
    l = Logger(Config)
    l.debug( msg )
    print(msg)

def run (repository):
    prefix_path = Config.repository[repository]['local']
    remote = Config.repository[repository]['remote']
    try:
        index_at = remote.index('@')
        index_colon = remote.index(':')
        remote_user = remote[:(index_at)]
        remote_host = remote[(index_at + 1):(index_colon)]
        remote_path = remote[(index_colon + 1):]
    except Exception, e:
        log_error("Failed to set initial variable" % e)
        exit( 1 )

    git = sh.git.bake( _cwd=prefix_path )

    # show status
    try:
        print git.status()
    except Exception, e:
        log_error( 'Failed to run status??: %s' % e )
        exit( 1 )

    # run commiter
    try:
        path_exec = os.path.join( path_origin, 'committer.py' )
        proc_commiter = subprocess.Popen( [path_exec, repository] )
        proc_commiter.communicate()
        if proc_commiter.returncode != 0:
            raise Exception ('Return code: %d' % proc_commiter.returncode)
    except Exception, e:
        log_error( 'Failed to run committer?: %s' % e )
        exit( 1 )

    # get current branch
    try:
        current_branch = git('symbolic-ref', 'HEAD', '--short').strip()
    except Exception, e:
        log_error(('Failed to issue git branch command: %s' % e))
        exit( 1 )
    if current_branch == 'master':
        log_error( "You may not want to push to `master` branch" )
        exit( 1 )

    # get remote branch name
    try:
        remote_branch = Config.repository[repository]['branches'][current_branch]
    except Exception, e:
        log_error(('"%s" is not on registered branch. Check ~/.tetherball/config.json' % current_branch))
        exit( 1 )

    # push from local to remote
    try:
        git.push()
    except Exception, e:
        log_error(('Failed to git-push: %s' % e))
        exit( 1 )        

    # work in remote
    ssh = spur.SshShell(
        hostname=remote_host,
        username=remote_user
    )

    # getting remote branch
    # result = ssh.run(['git', 'symbolic-ref', 'HEAD', '--short'], cwd=remote_path)
    result = ssh.run(['git', 'symbolic-ref', 'HEAD'], cwd=remote_path)
    if result.return_code != 0:
        log_error( 'Failed: %s - %s' % ('remote branch', result.stderr_output) )
        exit( 1 )
    try:
        current_remote_branch = '/'.join( result.output.split('/')[2:] )
    except Exception, e:
        log_error( 'Failed: %s - %s' % ('remote branch name fetching', e) )
        exit( 1 )

    # check the remote branch status
    result = ssh.run(['git', 'status'], cwd=remote_path)
    if result.return_code != 0:
        log_error( 'Failed: %s - %s' % ('remote branch status', result.stderr_output) )
        if not 'working directory clean' in result.output:
            log_error( 'Failed: remote branch is not cleaned' )
            exit( 1 )
    if current_remote_branch != remote_branch:
        result = ssh.run(['git', 'checkout', remote_branch], cwd=remote_path)
        if result.return_code != 0:
            log_error( 'Failed: %s - %s' % ('remote branch switch', result.stderr_output) )
            exit( 1 )

    # merge!
    result = ssh.run(['git', 'merge', current_branch], cwd=remote_path)
    if result.return_code != 0:
        log_error( 'Failed: %s - %s' % ('remote branch merge', result.stderr_output) )
        exit( 1 )
    log_error( 'Done!' )

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='Run Tetherball push and merger' )
    parser.add_argument( 'repository', type=str, help='Name of the repository registered to Tetherball' )
    args = parser.parse_args()
    repository = args.repository
    if not repository in Config.repository.iterkeys():
        log_error("`%s` doesn't seem to be registered to Tetherball." % repository)
        exit( 1 )

    run( repository )

