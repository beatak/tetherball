from cmd import Cmd
from watcher import Watcher
from notifier import Notifier

# http://docs.python.org/2/library/cmd.html
# http://stackoverflow.com/questions/10234595/python-cmd-module-parsing-values-from-line

class RunnerCmd(Cmd):
    # prompt
    # indentchars
    # lastcmd
    # intro
    # doc_header
    # misc_header
    # undoc_header
    # ruler
    # use_rawinput

    #def cmdloop(intro):
    #def Cmd.onecmd (str):
    #def default(line):
    #def completedefault (text, line, begin_index, end_index):
    #def precmd (line):
    #def postcmd (stop, line):
    #def preloop ():
    #def postloop ():

    prompt = '> '
    intro = 'OH HAIII'

    def set_config (self, config=''):
        print 'cmd confing: ' + config
 
    def onecmd(self, line):
        print 'one command'

    def do_foo(self, arg):
        print arg

if __name__ == '__main__':
    # should pass the config from here.
    config = 'foo'

    # n = Notifier( 'tether-ball' )
    # n.message( 'oh yes' )

    w = Watcher( config=config )
    w.start()
    w.stop()
    runner = RunnerCmd()
    runner.set_config( config )
    runner.cmdloop()

