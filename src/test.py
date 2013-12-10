
import os.path, argparse
import daemon
import psutil #pypy...

parser = argparse.ArgumentParser(description='Manage Tetherball application')
parser.add_argument(
    'command', 
    type=str, 
    nargs=1,
    help='start/stop/restart watching Tetherball')
args = parser.parse_args()

PATH_CWD = os.path.expanduser('~')
FILE_LOCKFILE = 'lockfile'

def run_command (command):
    PATH_TETHERBALL_BASE = os.path.join( PATH_CWD, '.tetherball' )
    PATH_TETHERBALL_LOCK = os.path.join( PATH_TETHERBALL_BASE, FILE_LOCKFILE )

    if os.path.exists( PATH_TETHERBALL_BASE ):
        if not os.path.isdir( PATH_TETHERBALL_BASE ):
            print "%s is not a directory? You may need to fix is manually" % PATH_TETHERBALL_BASE
            exit( 1 )
    else:
        os.mkdir( PATH_TETHERBALL_BASE )

    if command == 'start':
        command_start(PATH_TETHERBALL_LOCK)
    elif command == 'stop':
        command_stop(PATH_TETHERBALL_LOCK)
    else:
        command_stop(PATH_TETHERBALL_LOCK)
        command_start(PATH_TETHERBALL_LOCK)
    exit( 0 )

def command_start (lock):
    try:
        ret_code = daemon.createDaemon()
        pid = str( os.getpid() )
        run_notifier()
        file = open( lock, 'w' )
        file.write( pid )
        file.close()
    except Exception, e:
        print e
        exit( 1 )

def command_stop (lock):
    if not os.path.exists( lock ):
        print "It hasn't started yet?"
        exit( 1 )
    else:
        file_pid = open( lock, 'r' )
        pid = int( file_pid.read() )
        psutil.Process(pid).terminate()
        file_pid.close()
        os.unlink( lock )

        

def run_notifier ():
    from notifier import Notifier
    from fsevents import Observer, Stream
    n = Notifier(title='Tetherball testing')
    path = '/Users/tmizohata/Repository'

    def callback(FileEvent):
        # mask, cookie, event
        n.message( message=FileEvent.name)
        print FileEvent

    observer = Observer()
    observer.start()
    stream = Stream(callback, path, file_events=True)
    observer.schedule(stream)



if __name__ == "__main__":
    if args.command[0] in ('start', 'stop', 'restart'):
        run_command(args.command[0])
        exit( 0 )
    else:
        print "Unknow command: %s" % args.command[0]
        parser.print_help()
        exit( 1 )

