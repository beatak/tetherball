from notifier import Notifier
from fsevents import Observer, Stream

n = Notifier('fsevent test')
path = '/Users/tmizohata/Repository'
def callback(FileEvent):
    # mask, cookie, event
    n.message( message=FileEvent.name)
    print FileEvent

observer = Observer()
observer.start()
stream = Stream(callback, path, file_events=True)
observer.schedule(stream)

#question: how do i run this in deamon safely?
