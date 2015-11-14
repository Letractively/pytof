pytof helps you share your iPhoto pictures, and any pictures that are stored in a flat directory since version 0.3.0. It works on Mac, Windows and Linux.

IMPORTANT NOTICE. If you want to use pytof, the trunk is currently broken. Use [revision 361](https://code.google.com/p/pytof/source/detail?r=361). (Check out first, then svn up -r 361 does the trick).

# Web #

The default usage of pytof is to create an HTML gallery of your iPhoto albums. You can then put this generated folder online to share your pictures. There is even an ftp push option to automatically push your photo to your website.

# Emails #

For those who doesn't have a personal webpage, you can compress the album generated to an archive, and send it by email to your friends or family.

  * zip exporting (-z switch) is the simplest method. You just send a zip file to your fellow windows users.
  * tar exporting (-t switch) let you share pictures with Mac and Unix users.

Users will just have to double click their email attachments, and open the index.html files within the un-archived iPhoto album directory to view your pictures.

With the -s switch, you'll discard all the originals pictures, and your archive file will be way smaller, which means that most likely you'll be able to send it by emails to your friends or family !

# Web services #

We hope to provide soon a flickr push feature. Flickr let you share your pictures online with some neat features (commenting, geo-tagging, etc...). If there's a public API for Picassa one day that would be great also.

pytof uses a command line interface for now, but we'd like to provide a graphical user interface in the future.




















