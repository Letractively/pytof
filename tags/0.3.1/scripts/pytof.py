#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# Main file.
#

__revision__ = '$Id$  (C) 2006 GPL'
__author__ = 'Benjamin Sergeant'
__dependencies__ = []

import sys
sys.path.insert(1, '../pytof')

from log import loggers
# FIXME: find a way to get the file name in python
logger = loggers['pytof']

from os.path import expanduser, join, exists, basename, isabs, walk, isdir
from albumdataparser import AlbumDataParser, AlbumDataParserError
import os, sys
from utils import _err_, _err_exit, help, echo, log, GetTmpDir
from configFile import configHandler
import makepage, makefs
from cPickle import dump, load
from optparse import OptionParser
import tarfile
from shutil import rmtree
from ftp import ftpUploader
from ftplib import error_perm
from getpass import getuser, unix_getpass
from zipfile import ZipFile, ZIP_DEFLATED
from string import rstrip

# FIXME: (see issue 11)
__version__ = open('../VERSION').read().strip()

def getStringFromConsole(text, default = ''):
    value = raw_input('%s[%s]:' %(text, default))
    if not value:
        return default
    return value

def main(albumName, libraryPath, xmlFileName, outputDir,
         info, fs, tar, zip, ftp, strip_originals, fromDir):
    # init the config file
    conf = configHandler()
    if not conf.ok:
        _err_exit('Problem with the config file')
        
    # config file parameters
    if conf.hasLibraryPath() and not libraryPath:
        libraryPath = conf.getLibraryPath()
    else:
        conf.setLibraryPath(libraryPath)
        
    if conf.hasXmlFileName() and not xmlFileName:
        xmlFileName = conf.getXmlFileName()
    else:
        conf.setXmlFileName(xmlFileName)

    if outputDir == GetTmpDir():
        if conf.hasOutputDir():
            outputDir = conf.getOutputDir()
    else:
        conf.setOutputDir(outputDir)            

    if not fromDir:
        try:
            echo("Parsing AlbumData.xml")
            parser = AlbumDataParser(libraryPath, xmlFileName)
            xmlFileName = parser.xmlFileName
            
            # can we use the cached xml content ?
            # try to load our stuff from the cache if the xml wasn't modified
            cached = conf.canUseCache(xmlFileName)
            
            if cached:
                pickleFd = open(conf.pickleFilename)
                xmlData = load(pickleFd)
                pickleFd.close()
            else:
                xmlData = parser.parse()
                xmlData.libraryPath = libraryPath

            # writing the cached data to a file
            pickleFd = open(conf.pickleFilename, 'w')
            dump(xmlData, pickleFd)
            pickleFd.close()
                
            echo("\t[DONE]\n")

        except(AlbumDataParserError):
            _err_exit("Problem parsing AlbumData.xml")
    else:
        logger.info('generate gallery from photos in %s dir' % fromDir)
        xmlData = None
        albumName = basename(rstrip(fromDir, '/'))
        logger.info('albumName is %s' % albumName)

    up = 'pytof'
    topDir = join(outputDir, up, albumName)
    try:
        if not exists(topDir):
            os.makedirs(topDir)
    except (os.error):
        _err_exit('Cannot create %s' %(topDir))

    print 'output dir is %s' % (topDir)

    try:
        if info:
            print ('\n').join(xmlData.getAlbumList())
        else:
            if fs:
                makefs.main(albumName, topDir, xmlData)
            else:
                makepage.main(albumName, topDir, xmlData, strip_originals, fromDir)

            if tar:
                pwd = os.getcwd()
                os.chdir(join(outputDir, up))
                tarball = tarfile.open(albumName + '.tar', 'w')
                tarball.add(albumName)
                os.chdir(pwd)
                if not fs:
                    # FIXME: maybe pb here: see zip section
                    tarball.add(makepage.cssfile,
                                basename(makepage.cssfile))
                tarball.close()
                tarballFilename = join(outputDir, up, albumName + '.tar')
                logger.info('output tarball is %s' % (tarballFilename))

            if zip:
                def visit (z, dirname, names):
                    for name in names:
                        path = os.path.normpath(os.path.join(dirname, name))
                        if os.path.isfile(path):
                            # strip topDir from the fn in archive
                            # and replace by the album name
                            filename_in_archive = path.replace(topDir, albumName)
                            z.write(path, filename_in_archive)
                            logger.info("adding '%s'" % path)
                
                zip_filename = topDir + '.zip'
                z = ZipFile(zip_filename, "w",
                            compression=ZIP_DEFLATED)
                walk(topDir, visit, z)

                if not fs:
                    z.write(makepage.cssfile,
                            basename(makepage.cssfile))
                
                z.close()
                logger.info('output zipfile is %s' % (zip_filename))

            if ftp:

                logger.debug('Entering ftp code')
                fromConfig = False
                if conf.hasFtpParams():
                    answer = getStringFromConsole('Use last ftp parameters', 'y')
                    if answer == 'y':
                        host, user, passwd, remoteDir = conf.getFtpParams()
                        fromConfig = True        

                if not fromConfig:
                    # localhost is a preference for test
                    host = getStringFromConsole('Host', 'localhost')
                    user = getStringFromConsole('User', getuser())
                    passwd = unix_getpass()
                    remoteDir = getStringFromConsole('Remote directory', '')
                    if not isabs(remoteDir):
                        logger.error('Sorry: the remote drectory has to be an absolute path')
                        remoteDir = ''

                try:
                    ftpU = ftpUploader(host, user, passwd)
                except (error_perm):
                    logger.error('Incorrect ftp credentials')
                    sys.exit(1)
                if remoteDir:
                    if not ftpU.exists(remoteDir):
                        log('remote dir %s does not exist' % remoteDir)
                        remoteDir = ftpU.pwd()
                else:
                    remoteDir = ftpU.pwd()
                conf.setFtpParams(host, user, passwd, remoteDir)
                
                if tar:
                    ftpU.upload(tarballFilename,
                                join(remoteDir, basename(tarballFilename)))
                else:
                    # we'll have to mirror the whole dir
                    if not fs:
                        logger.debug('upload css')
                        ftpU.upload(makepage.cssfile,
                                    join(remoteDir, basename(makepage.cssfile)))
                    ftpU.cp_rf(topDir,
                               remoteDir)

    except (KeyboardInterrupt):

        if not info:
            if not fs:
                # os.remove(makepage.cssfile)
                # we should remove the css file if there aren't
                # any other exported albums left... hard to know,
                # may be stored in the rc file, under the Internal section.
                pass

            if exists(topDir):
                rmtree(topDir)

        _err_exit("\nAborted by user")


if __name__ == "__main__":

    # parse args
    usage = "usage: python %prog <options>"
    parser = OptionParser(usage=usage)
    
    parser.add_option("-a", "--album", dest="albumName", default='',
                      help="The iPhoto library album to process"),
    parser.add_option("-i", "--info",
                      action="store_true", dest="info", default=False,
                      help="Print info about the collection [default = %default]")
    parser.add_option("-o", "--output", dest="outputDir", default=GetTmpDir(),
                      help="The output directory [%default + out/ALBUMNAME]"),
    parser.add_option("-f", "--file-system",
                      action="store_true", dest="fs", default=False,
                      help="Extract album photo to OUTPUTDIR and stop")
    parser.add_option("-t", "--tar-archive",
                      action="store_true", dest="tar", default=False,
                      help="Create a tar archive from the exported datas")
    parser.add_option("-z", "--zip-archive",
                      action="store_true", dest="zip", default=False,
                      help="Create a tar archive from the exported datas")
    parser.add_option("-V", "--version",
                      action="store_true", dest="version", default=False,
                      help="display version")
    parser.add_option("-l", "--library", dest="libraryPath", default='',
                      help="The iPhoto library directory path"),
    parser.add_option("-x", "--xml-file", dest="xmlFileName", default='',
                      help="The iPhoto library XML file name"),
    parser.add_option("-u", "--ftp-upload",
                      action="store_true", dest="ftp", default=False,
                      help="Upload pytof output to a ftp site")
    parser.add_option("-s", "--strip-originals",
                      action="store_true", dest="strip_originals", default=False,
                      help="Remove the originals from the generated gallery Gallery will be way smaller")
    parser.add_option("-d", "--from-directory", dest="fromDir", default='',
                      help="The directory path for the gallery. Do not interact with iPhoto"),

    options, args = parser.parse_args()
    
    if options.version:
        print 'pytof version %s' % (__version__)
        sys.exit(0)

    if options.info: pass
    elif options.fromDir:
        if not isdir(options.fromDir):
            _err_exit('Not a directory: %s' % options.fromDir)
    elif not options.albumName:
        _err_exit('missing albumName argument')
            
    main(options.albumName, options.libraryPath,
         options.xmlFileName, options.outputDir,
         options.info, options.fs, options.tar,
         options.zip, options.ftp, options.strip_originals,
         options.fromDir)
