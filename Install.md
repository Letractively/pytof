## pytof ##

pytof is now a distutils friendly python package and can be installed, assuming you have python installed (the programming langage used for pytof), with a simple command.

### Mac ###

```
sudo python setup.py install
```

This will copy stuff to your system directory, so you'll either

### Unix ###

#### Prepackaged binaries ####

There are rpm (the first one has a nasty bug so you might wait for the 0.8.x with x > 0 for that. The following command should do the trick.

```
rpm -i pytof-<version>.rpm
```

The cool thing is that you can also cleanly remove the package with rpm (rpm -e).

If anyone wants to package the debian version I'd be glad to include it on the download page.

#### From source ####

Basically the same command as for Mac, but if you don't have sudo just type su: then your password, and next:

```
python setup.py install
```

This will need root

## Dependancies ##

For thumbnails creation pytof rely on the python imaging library (PIL), which itself rely on the libjpeg for low level jpeg handling. Both of them should be installed, and the process is quite simple. **New**: We can now fallback on pygtk or wxPython is any of those are installed. wxPython is installed by default on Mac Tiger, but the quality of the created thumbnail is bad, I have to look into that.

## Install dependancies using prepackaged binaries ##

### Mac ###

#### Panther ####

I made a PIL archive where PIL is compiled against a static libjpeg, so it should be self contained.
```
[100drine@gnocchi tmp]$ cd /Library/Python/2.3/    
[100drine@gnocchi 2.3]$ sudo curl -O http://pytof.googlecode.com/files/PIL-PPC-Panther-python-2.3.tar.bz2
[100drine@gnocchi 2.3]$ sudo bunzip2 -c PIL-PPC-Panther-python-2.3.tar.bz2 | tar xf -
```
When sudo ask you a password, type your user password.

#### Tiger ####

I also made tar files with everything installed, that you can install just like on OSX.

**[Intel](http://pytof.googlecode.com/files/PIL-Tiger-Intel.tgz) Mac** [Powe PC](http://pytof.googlecode.com/files/PIL-Tiger-PPC.tgz) Mac

### Linux ###

Under mandriva the package name is python-imaging.

### Solaris ###

Installing [PIL](http://www.blastwave.org/packages/pil) using [blastwave](http://www.blastwave.org) will  do all the job for you.

### Windows ###

  * Install [python](http://www.python.org/ftp/python/2.4.4/python-2.4.4.msi)
  * Install [PIL](http://effbot.org/downloads/PIL-1.1.6.win32-py2.4.exe)
  * For now the GUI is minimalistic so you'll have to type commands in a terminal. To
get a nice experience you should install [cygwin](http://www.cygwin.com/mirrors.html) which comes with [bash](http://www.gnu.org/software/bash/).

## Install dependancies from sources ##

The drawback is that you need to install the developper tools on the Mac, (a good 1Gigabyte dmg to download, hum ...) to get gcc that is required to build PIL and libjpeg. As there is a windows installer on the PIL site, you'd better use that one. And on Linux most likely you will have pre-packaged PIL and libjpeg, otherwise install gcc.

### Python eggs ###

Get the python eggs [runtime](http://peak.telecommunity.com/DevCenter/EasyInstall#installing-easy-install), and issue this command to install PIL (but you'll still have to compile a static libjpeg).

```
sudo easy_install -f http://www.pythonware.com/products/pil/ Imaging
```

I created an egg for Intel Tiger, that you can just copy to  if you do not have the developper tools, because that last command will require them to be installed. I think you just have to extract and copy the .egg terminated directory to your site-packages (mine is at `/System/Library/Frameworks/Python.framework/Versions/2.3/lib/python2.3/site-packages`). I'm not positive on that thought, as I am an egg user newbie.

### Automatic ###

The sources for the open source project were added to our sources in the deps
directory.  A simple **install.sh** script can be found in the deps directory.
To have a verbose output, run it like `sh -x install.sh`.
If you get pytof throught subversion you'll get those sources for free,
otherwise download them from the download page.

You'll just have to enter your account password as it calls sudo sometimes.

### Manual ###

Maybe install.sh won't work for you, so here are the steps to follow.

#### libjpeg ####

We should provide a tar file compiled on a MacTel with Tiger soon with the right file.
Grab that [here](ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v6b.tar.gz). I had a bad experience with the default configure, so I had to manually copy the header and the static library to /usr/local. You may have to download the developper tools from the main Apple website, but I think there's a default gcc there and it's all you need.

```
$ tar zxf jpegsrc.v6b.tar.gz
$ cd jpeg-6b
$ ./configure
$ sudo mkdir -p /usr/local/{include,lib}
$ sudo cp *.h /usr/local/include
$ sudo cp libjpeg.a /usr/local/lib
```

#### PIL ####

Grab the source code [here](http://effbot.org/downloads/Imaging-1.1.6.tar.gz), extract it and from the PIL main dir, issue that:

```
sudo python setup.py install
```

You should be good to go, and ready to play with pytof !!

## gtof ##

gtof is the name of the pytof graphical user interface. It is using the pygtk toolkit + libglade, so you'll have to install both of them.

### Linux ###

Just use your installer manager to get glade-3 and pygtk (urpmi, yum, apt-get).

### Windows ###

An all in one installer is being prepared by the pygtk fols, but for now:

#### Step by step ####

  * Install gtk+ and glade from [here](http://gladewin32.sourceforge.net/modules/news/). I used the 2.10.7 version.
  * Look for the Win32 Installer section in the pygtk [download](http://www.pygtk.org/downloads.html) page, and install those tree guys: PyCairo (1.2), PyGObject (2.12), PyGTK (2.10)

#### All in one installer ####

Some nice guy packaged python  + gtk + pygtk [together](http://aruiz.typepad.com/siliconisland/2006/12/allinone_win32_.html). Just download that big [installer](http://osl.ulpgc.es/~arc/gnome/pygtk-setup.exe), and you will get all gtof deps in a single step. Cool, no ?

### Mac ###

Fink / x11 is needed for now, but there may be a lighter process as there is now a non X11 gtk implementation on the Mac, which is good news.

## One click Installer ##

Of course in the near future we'd like to make a nice OS X package, so that no-one would have to experience tar and configure nice moments. There is already a cool windows setup.exe like installer that can be downloaded from the pytof download page.