## General ##

Here is the google code hosting [FAQ](http://code.google.com/hosting/faq.html).
If ou have ideas on how the service could be better, add notes [here](http://code.google.com/p/support/issues/list). Here the Zope svn [tips](http://www.zope.org/DevHome/Subversion/ZopeSVNFAQ), might be interesting.

## Subversion ##

### Importing ###

Here is how I imported the source code:

```
[bsergean@flanders pytof]$ svn import https://pytof.googlecode.com/svn/trunk --username bsergean
Authentication realm: <https://pytof.googlecode.com:443> Google Code Subversion Repository
Password for 'bsergean':
Adding         photo.py
Adding         makepage.py
Adding         README.txt
Adding         svn-commit.tmp
Adding         albumdataparser.py

Committed revision 13.
```

### Check out ###

```
[bsergean@flanders src]$ svn co https://pytof.googlecode.com/svn/trunk
Authentication realm: <https://pytof.googlecode.com:443> Google Code Subversion Repository
Password for 'bsergean':
A    trunk/photo.py
A    trunk/makepage.py
A    trunk/README.txt
A    trunk/svn-commit.tmp
A    trunk/albumdataparser.py
Checked out revision 15.
```

If you want to edit the wiki offline, it's possible as the wiki is under subversion also. Didn't do it yet but should be simple to figure out the svn path from [that](http://pytof.googlecode.com/svn/wiki/).
I just did that, you simply have to replace trunk with wiki ... the big bonnus
is that you can use your prefered editor to do that, and edit several files at
a time, fast, without the need to save (and wait) if you want to switch to
another wiki page.

### Branching ###

See this [note](http://svnbook.red-bean.com/en/1.1/ch04s02.html) from the subversion book. The following command create a branch, and . has to be under subversion (the previous command won't work, check the one from the Source Tab. Then commit and start working in your branch by _cding_ there.

```
[bsergean@marge1 pytof]$ svn copy trunk/ branches/makepages-scry
A         branches/makepages-scry
```

### Moving ###

If you move files or dirs around, it may fails sometimes and when you want to re-add your directories that you backuped somewhere, don't forget to erase all the .svn directories within the freshly to be added directories, otherwise commit will fails ... keep this in mind.

## Wiki ##

Quote from the FAQ:
```
What syntax are you using in the wiki?
    Our wiki syntax is inspired by the MoinMoin wiki syntax, and is more or less a subset of it. We've found that MoinMoin is one of the most popular open source wikis and provides a clean syntax for users. 
    Specific examples of how to use the wiki syntax are shown in the "Wiki Markup Help" box on the right-hand side of the wiki page creation and editing pages.
```

## Editors ##

Mathieu uses Eclipse with the pydev module, and Benjamin wants to learn vim. But as he's developping on Linux he's only using emacs actually ... anyway when debugging on the Mac those vim links are usefull.

### vim ###

  * [viewports](http://applications.linux.com/article.pl?sid=06/05/04/1544258&tid=13).
  * [buffers](http://www.vim.org/tips/tip.php?tip_id=135).

## Tools ##

Some tools were added in the tools directory.

  * svn2cl.pl produce a nice changelog from the svn directory
```
[100drine@gnocchi trunk]$ svn log . | perl tools/svn2cl.pl > ChangeLog
```
  * deps/install.sh is the script which compile and install the deps

## Downloads ##

With the script that google provide, you can do it from the command line. By default it won't be a featured download thought.

```
[bsergean@marge1 tools]$ python googlecode-upload.py -s 'Add the strip option to send emails with light gallery' -u bsergean -p pytof /home/bsergean/src/pytof/tags/0.2.0/dist/pytof-0.2.0.tar.gz
Please enter your googlecode.com password.
Note that this is NOT your main Gmail account password!
Password:
The file was uploaded successfully.
URL: http://pytof.googlecode.com/files/pytof-0.2.0.tar.gz
```