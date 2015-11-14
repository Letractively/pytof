Some dev notes working with subversion, based on the branch section in the subversion book.

# Working with features branches #

Here I describe how I worked on a new feature in a separate branch, to keep trunk stable, and how I merged this work to trunk then. The temporary branch, useless after the merge, was deleted.

## Branch creation ##

  * You can use the `copy` command to copy the trunk to a branch.
  * You can now work there.

## Merge ##

### Find out the branch the branch revision ###

Within the branch, just type:

```
[bsergean@marge1 makepages-scry]$ svn up .
At revision 85.
```

Every work should be checked in.

### Find out when the branch was created, using subversion log ###

If you haven't used a check in comment to mark that, subversion can help you to do that.

```
[bsergean@marge1 makepages-scry]$ svn log --verbose --stop-on-copy
------------------------------------------------------------------------
r85 | bsergean | 2006-12-23 21:14:33 -0500 (Sat, 23 Dec 2006) | 1 line
Changed paths:
   M /branches/makepages-scry/test/WebPageTest.py

unit test was not compiling
------------------------------------------------------------------------
r84 | bsergean | 2006-12-23 21:13:26 -0500 (Sat, 23 Dec 2006) | 1 line
Changed paths:
   M /branches/makepages-scry/pytof/makepage.py

some page had absolute path references
------------------------------------------------------------------------
r83 | bsergean | 2006-12-23 20:55:55 -0500 (Sat, 23 Dec 2006) | 1 line
Changed paths:
   M /branches/makepages-scry/pytof/makepage.py

per photo page had an absolute path
------------------------------------------------------------------------
r82 | bsergean | 2006-12-23 20:51:04 -0500 (Sat, 23 Dec 2006) | 1 line
Changed paths:
   M /branches/makepages-scry/pytof/makepage.py
   M /branches/makepages-scry/pytof/photo.py
   M /branches/makepages-scry/scripts/pytof.py
   M /branches/makepages-scry/test/WebPageTest.py

scry navigation is almost OK ... just need to parse EXIF datas
------------------------------------------------------------------------
r81 | bsergean | 2006-12-23 16:43:22 -0500 (Sat, 23 Dec 2006) | 1 line
Changed paths:
   M /branches/makepages-scry/pytof/makepage.py
   M /branches/makepages-scry/pytof/utils.py
   M /branches/makepages-scry/scripts/pytof.py
   A /branches/makepages-scry/share/scry
   A /branches/makepages-scry/share/scry/PhotoPage.html
   M /branches/makepages-scry/test/WebPageTest.py

progress on the scry navigation side
------------------------------------------------------------------------
r80 | bsergean | 2006-12-23 13:20:40 -0500 (Sat, 23 Dec 2006) | 1 line
Changed paths:
   M /branches/makepages-scry/scripts/pytof.py

cleanup comments
------------------------------------------------------------------------
r79 | bsergean | 2006-12-23 13:10:58 -0500 (Sat, 23 Dec 2006) | 1 line
Changed paths:
   M /branches/makepages-scry/pytof/albumdataparser.py
   M /branches/makepages-scry/pytof/makepage.py
   M /branches/makepages-scry/pytof/utils.py
   M /branches/makepages-scry/scripts/pytof.py
   A /branches/makepages-scry/tools/googlecode-upload.py

switch to optparse, see cleanup issue 7
------------------------------------------------------------------------
r77 | bsergean | 2006-12-23 04:23:43 -0500 (Sat, 23 Dec 2006) | 1 line
Changed paths:
   A /branches/makepages-scry/test/WebPageTest.py

yet another dummy test file
------------------------------------------------------------------------
r76 | bsergean | 2006-12-23 04:16:52 -0500 (Sat, 23 Dec 2006) | 1 line
Changed paths:
   M /branches/makepages-scry/pytof/makepage.py
   M /branches/makepages-scry/pytof/utils.py
   M /branches/makepages-scry/setup.py
   A /branches/makepages-scry/share/scry.css

all the thumbnails on the same page
------------------------------------------------------------------------
r75 | bsergean | 2006-12-23 03:16:02 -0500 (Sat, 23 Dec 2006) | 1 line
Changed paths:
   A /branches/makepages-scry (from /trunk:73)

created a branch to work on the scry-like exporting
------------------------------------------------------------------------
```

So the branch was created at revision **75**.

### dry-run merge, from the trunk ###

```
[bsergean@marge1 trunk]$ svn merge --dry-run -r 75:85 https://pytof.googlecode.com/svn/branches/makepages-scry
A    test/WebPageTest.py
A    tools/googlecode-upload.py
U    pytof/photo.py
U    pytof/makepage.py
U    pytof/utils.py
U    pytof/albumdataparser.py
A    share/scry
A    share/scry/PhotoPage.html
A    share/scry.css
U    scripts/pytof.py
U    setup.py
```

Check that everything works, then remove the dry run option to do the actual merge.

# Create release branch #

## Working branch ##

```
[bsergean@marge1 pytof]$ svn copy trunk/ branches/0.0.2
A         branches/0.0.2
[bsergean@marge1 pytof]$
[bsergean@marge1 pytof]$
[bsergean@marge1 pytof]$ svn copy branches/0.0.2 tags/0.0.2
svn: Cannot copy or move 'branches/0.0.2': it is not in the repository yet; try committing first
[bsergean@marge1 pytof]$ svn commit -m 'create 0.0.2 branch'
Adding         branches/0.0.2
Adding         branches/0.0.2/pytof/albumdataparser.py
Adding         branches/0.0.2/pytof/makepage.py
Adding         branches/0.0.2/pytof/photo.py
Adding         branches/0.0.2/pytof/utils.py
Adding         branches/0.0.2/scripts/pytof.py
Adding         branches/0.0.2/setup.py
Adding         branches/0.0.2/share/scry
Adding         branches/0.0.2/share/scry.css
Adding         branches/0.0.2/test/WebPageTest.py
Adding         branches/0.0.2/tools/googlecode-upload.py
Sending        trunk/setup.py
Transmitting file data ..
Committed revision 87.
[bsergean@marge1 pytof]$
[bsergean@marge1 pytof]$
```

## Create tag from branch ##

Then you tag, or snapshot the release branch, and you can create a package from that snaphot. Ya shall not work there, it's just used for release engineering. All work should be done in the branch.

```
[bsergean@marge1 pytof]$ svn copy branches/0.0.2 tags/0.0.2
A         tags/0.0.2
[bsergean@marge1 pytof]$
[bsergean@marge1 pytof]$
[bsergean@marge1 pytof]$ svn commit -m 'create 0.0.2 tag from 0.0.2 branch'
Adding         tags/0.0.2

Committed revision 88.
```

## Properties ##

Usefull when you want to revert a property, like an executable property that you set on a source file. From the subversion [book](http://svnbook.red-bean.com/en/1.0/ch07s02.html).

# Links #

[subversion](http://svnbook.red-bean.com/en/1.1/ch04s04.html)
[Working with branches](http://www.dehora.net/journal/2006/02/subversion_tips_dealing_with_branches.html)