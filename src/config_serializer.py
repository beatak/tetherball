from json import JSONEncoder

class MyEncoder(JSONEncoder):
    def default(self, o):
        try:
            result = {}
            for key in o.__dict__.keys():
                # print "\t %s: %s" % (key, str(o.__dict__[key]))
                if not key.startswith('__'):
                    result[key] = o.__dict__[key]
                # else:
                #     print "omit!"
            return result
        except Exception, e:
            print e
        return

