See Issues page instead, this is old content.

## Cleanup ##

  * Include everything but function or classes in a main() in the main file
  * Be able to export to a fs (to be used by scry next)
  * Have an option handler (getopt style)
  * Start to document the project (use Restructured Text for the format), also add pydoc markup
  * Create a tar file with jpeg (/usr/local/include/all header files from the jpeg lib + /usr/local/lib/libjpeg.a) is enough)
  * Makes pyphoto a valid python module. Add a setup.py plus the files needed to do so.
  * Check the date thing (with the Apple timestamp computed from year 2001) with Mathieu
  * Update the dir, don't recreate the whole thing.
  * Have a config file with the name of the place where we want to export our stuff (a python file, see orm)
  * The default output dir should be something name pytof and be inside `public_html` dir
  * Have an export to tar, or tar.gz when people want to upload their content to a remote site.
  * Create an index.html file containing links to the multiple html files, (should be an option, maybe the user want to have all thumbnails in the same html page).

## Admin ##

  * Figure out how to make subversion store the password on Linux
  * Try to add an alpha version and make it downloadable in the Download tab.

## Defensive code ##

  * Check that PIL install support jpeg at runtime before crashing.
  * Create the out dir if no such thing exist (done)
  * Conf: have a param to set where is the AlbumData.xml (maybe not in Picture/iPhoto)

## Testing ##

  * Unit testing: Add xml tests files (small library with, and our big libraries)
  * Multiple templates for the html export: Option to choose the css or the template look.

## Long term ##

  * Create an installer
  * ncurses (geek mode) or pyobjc user interface
  * Have an option to make a whole library backup (fs export for every gallery)
