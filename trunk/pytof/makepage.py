#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
# $Id$
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# Main file.
#

__revision__ = '$Id$  (C) 2006 GPL'
__author__ = 'Mathieu Robin'

from log import logger
from os.path import expanduser, join, exists, basename
from albumdataparser import AlbumDataParser, AlbumDataParserError, AlbumDataFromDir
import os, sys
from utils import _err_, _err_exit, echo, ProgressMsg
from shutil import copy

# globals ... bouhhhh
css = 'scry.css'
cssfile = join(os.pardir, 'share', css)
templateDir = join(os.path.pardir, 'templates')

def Template(template, data, output):
    from ezt import Template
    
    pytofTemplate = Template(template)
    wfile = open(output, 'w')
    pytofTemplate.generate(wfile, data)

def makePhotoPage(photo, topDir, prev, next, strip_originals):
    '''
    Should have a next and back with thumbnails
    FIXME: strip_originals is not implemented
    '''
    dico = {}
    dico['title'] = 'My title'
    dico['width'] = str(photo.width)
    dico['height'] = str(photo.height)
    dico['size'] = str(photo.sizeKB)
    dico['exif_infos'] = ('</br>').join(photo.exif_infos)
    dico['preview'] = join('preview', 'pv_' + photo.id + photo.getFileType())
    dico['preview_filename'] = basename(dico['preview'])
    dico['prev'] = prev.id + '.html'
    dico['prev_thumb'] = join('thumbs',   'th_' + prev.id + prev.getFileType())
    dico['next'] = next.id + '.html'
    dico['next_thumb'] = join('thumbs',   'th_' + next.id + next.getFileType())

    original = join('photos', photo.id + photo.getFileType())
    if strip_originals:
        original = ''
    dico['original'] = original

    Template(join(templateDir, 'photo_per_page.ezt'),
             dico, join(topDir, photo.id) + '.html')

def main(albumName, topDir, xmlData, strip_originals,
         fromDir, progress = ProgressMsg(0, sys.stderr)):
    logger.info('strip_originals = %s' % strip_originals)

    data = xmlData
    if fromDir:
        data = AlbumDataFromDir(fromDir)

    leafDirs = ['photos', 'preview', 'thumbs']
    dirs = []
    for leafDir in leafDirs:
        Dir = join(topDir, leafDir)
        dirs.append(Dir)
        if not os.path.exists(Dir):
            try:
                os.makedirs(Dir)
            except (os.error):
                _err_exit('Cannot create %s' %(Dir))

    # FIXME: how do we get the package install path, to retrieve
    # the resource dir next ...quick hack for now
    logger.info(cssfile)
    if not exists(cssfile):
        _err_('No css file was found: HTML files look and feel will be bad')
    else:
        copy(cssfile, join(topDir, os.pardir, css))

    logger.info(topDir)

    thumbs = []
    class Thumb:
        def __init__(self, page, image):
            self.page = page
            self.image = image
        
    logger.info("Writing pictures\n")
    
    photos = data.getPicturesIdFromAlbumName(albumName)
    progress.target = len(photos)
    for i in xrange(len(photos)):

        pic_id = photos[i]
        logger.debug('processing photo %s' % pic_id)
        
        photo = data.getPhotoFromId(pic_id)
        prev = data.getPhotoFromId(photos[i-1])
        try:
            next = data.getPhotoFromId(photos[i+1])
        except (IndexError):
            # ok I know it's crappy programming :)
            next = data.getPhotoFromId(photos[0])

        if not strip_originals:
            photo.saveCopy(dirs[0])
        photo.makePreview(dirs[1], 640)
        photo.makeThumbnail(dirs[2])

        # FIXME: makePhotoPage return photoPageName which shoule be
        # modified to HTML/123.html. We would only have to create
        # a dir HTML, change the links in the index to HTML/123.html
        # and create the per page file in HTML/123.html
        makePhotoPage(photo, topDir,
                      prev, next, strip_originals)
        thumbs.append(Thumb(photo.id + '.html',
                            join('thumbs', 'th_' + photo.id + photo.getFileType())))
        progress.Increment()

    dico = {}
    dico['title'] = albumName
    dico['thumbs'] = thumbs

    Template(join(templateDir, 'gallery_index.ezt'),
             dico, join(topDir, 'index') + '.html')
