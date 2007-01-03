#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************

__revision__ = '$Id$  (C) 2006 GPL'
__author__ = 'Benjamin Sergeant'

import sys
sys.path.insert(1, '../pytof')

import unittest
import os
from os import remove, walk, chdir, getcwd
from utils import GetTmpDir
from photo import Photo
from photo import EXIF_tags
from shutil import copy, rmtree
from tempfile import mkdtemp, mktemp
from os.path import join

def prune(tag, key):
    return str(tag[key])[0:-1]

def get_key(file, key, prune = False):
    tags = EXIF_tags(file)
    if key:
        if tags.has_key(key):
            if prune:
                return str(tags[key])[0:-1]
            else:
                return tags[key]

def print_tags(file):
    tags = EXIF_tags(file)
    for i in tags:
        if i not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename'):
            print '%s: %s' % (i, tags[i])

class EXIF_TC(unittest.TestCase):
    '''
    This test needs some pictures in the data directory
    '''
    def setUp(self):
        self.tempdir = mkdtemp()
        self.exim1 = join('data', 'exim1.jpg')
        self.exim2 = join('data', 'Rotated_90_CW_thumb.jpg')
        self.exim3 = join('data', 'Rotated_90_CW.jpg')

    def tearDown(self):
        rmtree(self.tempdir)

    def test_exim1_print(self):
        verbose = False
        if verbose:
            print_tags(self.exim1)
              
    def test_exim1_assert_values(self):

        tags = EXIF_tags(self.exim1)
        self.assert_( prune(tags, 'Image Model') == 'PENTAX Optio S5i' )
        self.assert_( prune(tags, 'Image Make') == 'PENTAX Corporation' )

        self.assert_( str(tags['EXIF DateTimeOriginal']) == '2005:04:10 17:52:16' )
        self.assert_( str(tags['EXIF Flash']) == 'Off' )

        photo = Photo(self.exim1)
        print ('\n').join(photo.EXIF_infos())

    def test_exif_stripped_picture(self):
        # Nothing will be printed since PIL remove the exif infos
        # on this data picture
        # FIXME: we should create it
        print_tags(self.exim2)

    def test_exif_assert_picture_is_rotated(self):
        key = 'Image Orientation'
        value = 'Rotated 90 CW'
        valueFromFile = str(get_key(self.exim3, key))
        print 'valueFromFile =', valueFromFile
        self.assert_ (valueFromFile == value)

    def _auto_rotate_thanks_to_exif(self, thumb = True):

        tgetDir = 'thumbs'
        if not thumb:
            tgetDir = 'preview'
        
        tmpFile = join(self.tempdir, 'toto.jpg')
        copy(self.exim3, tmpFile)

        oldpwd = getcwd()
        chdir(self.tempdir)
        
        photo = Photo(tmpFile)
        tmpDir = join(self.tempdir, tgetDir)
        os.mkdir(tmpDir)

        if not thumb:
            photo.makeThumbnail(tgetDir)
        else:
            photo.makePreview(tgetDir)

        for d in walk(self.tempdir):
            print d

        # uncomment to get this picture and check it (I use the handy xv)
        #copy(photo.thumbPath, '/tmp/thumb.jpg')

        chdir(oldpwd)

    def test_auto_rotate_thumbnail_thanks_to_exif(self):
        self._auto_rotate_thanks_to_exif(thumb = True)
    
    def test_auto_rotate_preview_thanks_to_exif(self):
        self._auto_rotate_thanks_to_exif(thumb = False)

if __name__ == "__main__":
    unittest.main()
