# this will be killed, probably

from notifier import Notifier
from fsevents import Observer, Stream

class Watcher:
    def __init__ (self, config=''):
        # do some crazy init
        print 'watcher initing: ' + config
        self.load_config()
        self.check_status()

    def load_config (self):
        # yo config
        print 'load config'

    def check_status (self):
        print 'checking status'


    def start (self):
        print 'start watching'
        # start watching

    def stop (self):
        print 'stop wathcing'
        # stop watching

    def store (self):
        print 'store the value'
        # store path infos based on the



# observer = Observer()
# observer.start()

# def callback(FileEvent):
#     ...

# stream = Stream(callback, path)
# observer.schedule(stream)
