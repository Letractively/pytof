#!/usr/bin/env python

'''
Write user sent content to a file that is read at each request ...
We should lock it in set_msg when writting
'''

import web
from base64 import urlsafe_b64decode
from time import time
from os.path import exists

com_fn = 'chat_com'

urls = (
  '/set_msg', 'set_msg',
  '/up', 'up',
  '/all', 'all')

messages = []

class up:
    def GET(self):
        return ''

class all:
    def GET(self):

        if not exists(com_fn): return 'Empty'

        d = web.input()
        user      = urlsafe_b64decode(d.user)
        index     = int(d.index)

        text = []
        for i,l in enumerate(messages):
            tokens = l.split(',')

            db_user      = tokens[0]
            msg          = urlsafe_b64decode(tokens[1])

            if msg and i >= index and db_user != user:
                text.append(db_user + '> ' + msg)

        if not len(text): return 'Empty'
        else: 
            text.insert(0,str(i))
            ret_text = '\n'.join(text)
            return ret_text

class set_msg:
    def GET(self):
        d = web.input()
        msg = d.msg
        user = d.user

        m = '%s,%s\n' % (user, msg)
        messages.extend([m])
        
        log  = 'Msg: ' + msg + ' received from ' + user + '\n'
        return log

app = web.application(urls, globals(), web.reloader) # There's web.profiler too

if __name__ == "__main__": 
    app.run()

# vim: set tabstop=4 shiftwidth=4 expandtab :
