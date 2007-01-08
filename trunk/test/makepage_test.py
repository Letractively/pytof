#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************

__revision__ = '$Id$  (C) 2004 GPL'
__author__ = 'Benjamin Sergeant'

import os
from utils import GetTmpDir
from makepage import WebPage, PhotoWebPage
from unittest import TestCase

class PhotoWebPageTest(TestCase):
    def testWritePage(self):
        foo = os.path.join(GetTmpDir(), 'foo')
        bar = os.path.join(GetTmpDir(), 'bar')

        wp = WebPage(foo, 'testpage')
        wp.writePage()

        wp = PhotoWebPage(bar, 'bar', 'home.html')

        # addSkeleton use a dictionnary now
        #wp.addSkeleton(12, 12, 1000, ['EXIF infos'], 'back.jpg', 'original',
        #               'prev', 'pv_prev', 'next', 'pv_next')
        wp.writePage()

        # here we could try to fetch the photo link from the page
        # and compare the size to check that
        # original_size > medium_size > thumbnail_size

        self.assert_(True)