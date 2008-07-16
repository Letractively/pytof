#!/usr/bin/env python

from urllib import urlopen
from time import sleep
from sys import argv, stdout, exit
from getpass import getuser
from time import time
from base64 import urlsafe_b64encode
from threading import Thread
from optparse import OptionParser
from os import linesep

from Tkinter import Entry, Frame, BOTH, YES, WORD
from ScrolledText import ScrolledText

class ChatClient:
    def __init__(self, server_host, user):
        if server_host == None:
            self.server_host = 'localhost'
        else:  
            self.server_host = server_host

        self.user = user
        port = '8080'
        self.urlbase = 'http://' + self.server_host + ':' + port + '/' 
        # self.urlbase = 'http://10.0.0.2/~benjadrine/cgi-bin/chat_server.py/'
        # self.urlbase = 'http://lisa1.corp.adobe.com/chat/'

        self.ok = True
        try:
            url = self.urlbase + 'up'
            urlopen(url)
        except (IOError):
            self.ok = False

        self.buffer = ''

    # Server request:
    def get_all(self, user):

        url = self.urlbase + 'all' + '?'
        fmt = ''
        fmt += 'user=%s' # Watch out / last one does not have a &
        args = fmt % (
                user)
        url += args

        data = urlopen(url).read()
        if data != 'Empty' and data != 'internal server error':
            self.buffer += '\r' + data + '\n'
            return True
        else:
            return None

    def flush_buffer(self):
        if self.buffer:
            stdout.write(self.buffer)
            stdout.flush()
            stdout.write(self.user + '> ')
            self.buffer = ''

    # Server request:
    def send_text(self, text, user):

        url = self.urlbase + 'set_msg' + '?'
        fmt = ''
        fmt += 'msg=%s&'
        fmt += 'user=%s' # Watch out / last one does not have a &
        args = fmt % (
                urlsafe_b64encode(text), 
                user)
        url += args
        data = urlopen(url).read()

# Update screen every seconds with what 
# friends are writting (or nothing)
class MyThread(Thread):

    def run(self):

        global user

        # We need self.quit to stop the program
        # by setting it to True
        self.quit = False 

        while not self.quit:
            cc.get_all(user)
            sleep(1)

class ChatInterpreter():

    def __init__(self, cc, user):
        self.cc = cc
        self.user = user

    def loop(self):

        # The writting thread
        self.t = MyThread()
        self.t.start()

        # Display first prompt
        stdout.write(self.user + '> ')

        while True:
            try:
                text = raw_input()
                stdout.write(self.user + '> ')
                stdout.flush()
            except(EOFError,KeyboardInterrupt): # Bye bye
                print
                return

            self.cc.flush_buffer()
            if text:
                self.cc.send_text(text, self.user)

class TkChat():

    def __init__(self, cc, user):
        self.cc = cc
        self.user = user

    def loop(self):

        frame = Frame()
        frame.pack(fill=BOTH, expand=YES)

        # All sub-widgets
        entry = Entry(frame)
        text = ScrolledText(frame, width=76, height=25, wrap=WORD)

        entry.pack(fill=BOTH, expand=YES)

        def my_print(arg):
            data = entry.get() + '\n'
            entry.delete(0, 100)
            text.insert("end", data)

        entry.bind('<Return>', my_print)

        text.pack(fill=BOTH, expand=YES)
        text.focus()
        frame.master.title("Diacritical Editor")
        frame.mainloop()

        return
        # The writting thread
        self.t = MyThread()
        self.t.start()

if __name__ == "__main__": 
    
    # parse args
    parser = OptionParser(usage = "usage: %prog <options>")

    host = None
    user = ''
    parser.add_option("-s", "--host", dest="host",
            help="The host plus port number where the server is running")
    parser.add_option("-l", "--username", dest="user", default=getuser(),
            help="Your user name")
    options, args = parser.parse_args()
    user = options.user
    host = options.host

    # Start
    cc = ChatClient(host, user)
    if not cc.ok:
        print 'Chat server down'
        exit(1)

    # ci = ChatInterpreter(cc, options.user)
    ci = TkChat(cc, options.user)
    ci.loop()
    # ci.t.quit = True

# vim: set tabstop=4 shiftwidth=4 expandtab :
