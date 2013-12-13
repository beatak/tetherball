
import os.path, argparse, subprocess
import psutil #pypy...

from config import Config
import daemon
from data import Data

path_origin = os.path.dirname( os.path.abspath( __file__ ) )

def run_command (command):
    # fixme: probably I should remove LOCK || not used anymore
    if command == 'start':
        command_start()
    elif command == 'stop':
        command_stop()
    else:
        command_stop()
        command_start()
    exit( 0 )

def command_start ():
    for name in Config.repository:
        path_exec = os.path.join( path_origin, 'runner.py' )
        path_local = str( Config.repository[name]['local'] )
        try:
            # this strcuture make name without a space...
            subprocess.call(' '.join( [path_exec, path_local, '--name', name] ), shell=True)
        except Exception, e:
            print "Failed to spawn a new process: %s" % e

def command_stop ():
    try:
        procs = os.listdir( Config.PATH_TETHERBALL_PROC )
        for proc in procs:
            path_proc = os.path.join( Config.PATH_TETHERBALL_PROC, proc )
            f = open( path_proc , 'r' )
            pid = int( f.read() )
            f.close()
            psutil.Process( pid ).terminate()
            os.unlink( path_proc )
    except Exception, e:
        print "Failed to stop daemons: %s" % e
        exit( 1 )

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description='Manage Tetherball application' )
    parser.add_argument( 'command', type=str, nargs=1, help='start/stop/restart watching Tetherball' )
    args = parser.parse_args()

    if args.command[0] in ('start', 'stop', 'restart'):
        run_command(args.command[0])
    else:
        print "Unknow command: %s" % args.command[0]
        parser.print_help()
        exit( 1 )
