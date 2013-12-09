from subprocess import call

TN_PATH = '/usr/local/bin/terminal-notifier'

class Notifier():
    def __init__ (self, title='Notifier'):
        self.title = title

    def message (self, message='nothing', open_url=None, execute_command=None):
        args = [TN_PATH]
        args.append( ('-message "%s"' % message) )

        if open_url:
            args.append( ('-open "%s"' % open_url) )

        if execute_command:
            args.append( ('-execute "%s"' % execute_command) )

        _c = ' '.join(args)
        call( _c, shell=True)

if __name__ == '__main__':
    Notifier().message()

