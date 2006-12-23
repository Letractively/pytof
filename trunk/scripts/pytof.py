#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
# $Id: makepage.py 42 2006-12-20 19:43:06Z bsergean $
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# Main file.
#

__revision__ = '$Id: makepage.py 42 2006-12-20 19:43:06Z bsergean $  (C) 2006 GPL'
__author__ = 'Benjamin Sergeant'
__dependencies__ = []

import sys
sys.path.insert(1, '../pytof')

from os.path import expanduser, join, exists
from albumdataparser import AlbumDataParser, AlbumDataParserError
import os, sys, getopt
from utils import _err_, _err_exit, help, echo, log
from configFile import getConfDirPath, getConfFilePath, canUseCache
import makepage, makefs
from cPickle import dump, load
from ConfigParser import RawConfigParser

# FIXME: (see issue 11)
__version__ = '0.0.1'

def main(albumName, libraryPath, xmlFileName, info, fs):
    try:
        echo("Parsing AlbumData.xml")
        parser = AlbumDataParser(libraryPath, xmlFileName)
        xmlFileName = parser.xmlFileName
        # can we use the cached xml content ?

        pickleFilename = join(getConfDirPath(), 'xmlData.pickle')
        log(pickleFilename)

        # try to load our stuff from the cache if the xml wasn't modified
        cached = canUseCache(xmlFileName)

        if cached:
            pickleFd = open(pickleFilename)
            xmlData = load(pickleFd)
            pickleFd.close()
        else:
            xmlData = parser.parse()
            xmlData.libraryPath = libraryPath

        # writing the cached data to a file
        if cached:
            pickleFd = open(pickleFilename, 'w')
            dump(xmlData, pickleFd, 2)
            pickleFd.close()
        
        echo("\t[DONE]\n")
    except(AlbumDataParserError):
        _err_exit("Problem parsing AlbumData.xml")

    topDir = join(outputDir, 'out', albumName)
    try:
        if not exists(topDir):
            os.makedirs(topDir)
    except (os.error):
        _err_exit('Cannot create %s' %(topDir))

    print 'output dir is %s' % (topDir)

    if info:
        print ('\n').join(xmlData.getAlbumList())
    else:
        if fs:
            makefs.main(albumName, topDir, xmlData)
        else:
            makepage.main(albumName, topDir, xmlData)


if __name__ == "__main__":

    class BadUsage: pass
    try:
        libraryPath = ''
        xmlFileName = ''
        albumName = ''

        import tempfile
        # mktemp has to be called once for tempdir to be initalized !!
        tempfile.mktemp()
        outputDir = tempfile.tempdir
        fs = False
        info = False

        # parse args
        opts, args = getopt.getopt(sys.argv[1:], 'ifVhl:x:a:o:')

        for opt, val in opts:
            # be carefull with the elif
            # when you change param order ...
            if opt == '-i':
                info = True
            elif opt == '-f':
                fs = True
            elif opt == '-V':
                print 'pytof version %s' % (__version__)
                sys.exit(0)
            elif opt == '-h':
                raise BadUsage
            elif opt == '-l':
                libraryPath = val
            elif opt == '-x':
                xmlFileName = val
            elif opt == '-a':
                albumName = val
            elif opt == '-o':
                outputDir = val
            else:
                _err_('Bad arg: %s' %(opt))
                raise BadUsage

        if not albumName and not info:
            _err_('missing albumName argument')
            raise BadUsage

        main(albumName, libraryPath, xmlFileName, info, fs)

    except (KeyboardInterrupt):
        _err_exit("Aborted by user")

    except (getopt.error, BadUsage):
        help(""" 
%s : Export iPhoto library

usage : python pytof.py <options>
OPTIONS | -a <name> : album name
        | -l <dir> : iPhoto library path
        | -o <dir> : output dir (default to /tmp)
        | -v : display pytof version
        | -h : display this text
        | -i : print info about the collection
        | -f : extract album photo to a dir and stop
        """,
                       __revision__,
                       __dependencies__,
                       __author__)
