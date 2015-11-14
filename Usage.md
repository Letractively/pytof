After install you should have the ctof.py and gtof.py copied in your PATH.

## CLI ##

The cli (command line interface) is called ctof.py, and it's text based.

```
[benjadrine@ravioli trunk]$ ctof.py --help
usage: python ctof.py <options>

options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -aALBUMNAME, --album=ALBUMNAME
                        The iPhoto library album to process
  -i, --info            Print info about the collection [default = %default]
  -oOUTPUTDIR, --output=OUTPUTDIR
                        The output directory [%default + pytof/ALBUMNAME]
  -f, --file-system     Extract album photo to OUTPUTDIR and stop
  -t, --tar-archive     Create a tar archive from the exported datas
  -z, --zip-archive     Create a tar archive from the exported datas
  -v, --verbose         Report a number of information
  -lLIBRARYPATH, --library=LIBRARYPATH
                        The iPhoto library directory path
  -xXMLFILENAME, --xml-file=XMLFILENAME
                        The iPhoto library XML file name
  -u, --ftp-upload      Upload pytof output to a ftp site
  -s, --strip-originals
                        Remove the originals from the generated gallery Gallery
                        will be way smaller
  -dFROMDIR, --from-directory=FROMDIR
                        The directory path for the gallery. Do not interact
                        with iPhoto
  -cSTYLE, --gallery-style=STYLE
                        The style of the HTML gallery.
  -p, --profile         Enable python profile module profiling
                        [default=%default]
```

Here is a sample output from a simple use of pytof.

```
[benjadrine@ravioli trunk]$ ctof.py -a mes-vacances-postales
output dir is /Users/benjadrine/pytof/mes-vacances-postales

100% - (3 processed out of 3) 
```

And here is what it did create:

```
[benjadrine@ravioli trunk]$ find /Users/benjadrine/pytof/mes-vacances-postales
/Users/benjadrine/pytof/mes-vacances-postales
/Users/benjadrine/pytof/mes-vacances-postales/.magic
/Users/benjadrine/pytof/mes-vacances-postales/2124.html
/Users/benjadrine/pytof/mes-vacances-postales/2154.html
/Users/benjadrine/pytof/mes-vacances-postales/2155.html
/Users/benjadrine/pytof/mes-vacances-postales/index.html
/Users/benjadrine/pytof/mes-vacances-postales/photos
/Users/benjadrine/pytof/mes-vacances-postales/photos/2124.jpg
/Users/benjadrine/pytof/mes-vacances-postales/photos/2154.jpg
/Users/benjadrine/pytof/mes-vacances-postales/photos/2155.jpg
/Users/benjadrine/pytof/mes-vacances-postales/preview
/Users/benjadrine/pytof/mes-vacances-postales/preview/pv_2124.jpg
/Users/benjadrine/pytof/mes-vacances-postales/preview/pv_2154.jpg
/Users/benjadrine/pytof/mes-vacances-postales/preview/pv_2155.jpg
/Users/benjadrine/pytof/mes-vacances-postales/thumbs
/Users/benjadrine/pytof/mes-vacances-postales/thumbs/th_2124.jpg
/Users/benjadrine/pytof/mes-vacances-postales/thumbs/th_2154.jpg
/Users/benjadrine/pytof/mes-vacances-postales/thumbs/th_2155.jpg
```

## GUI ##

The minimalistic GUI is called gtof.py, and implement (only) the -d feature of ctof, creating a gallery from a set of pictures within a directory.