# script.artwork.loader

This Kodi addon will add local artwork to the Kodi database for movies.

It can add the following artwork types:
- clearlogo
- clearart
- banner
- discart

Kodi itself cannot add these artwork types to the database at the time of writing (Kodi 16.1 or earlier). It CAN add poster and fanart via the nfo file, but not e.g. a clearlogo.

The "artwork downloader" always downloads files from e.g. fanart.tv, but has no option to load "sidecar" images from disk.

This addon expects the artwork files to be "sidecar" files, so in the same folder as the movie and named like this:

- c:\movies\a.mp4
- c:\movies\a-logo.png

or
- //there/are/movies/here/movie1.mkv
- //there/are/movies/here/movie1-art.png

This is different from the "artwork downloader", which can load local files, but expects each movie to be in its own folder with a generic "logo.png" file. 

The "artwork loader" expects each image to be named after the movie and in the same folder as the movie, but all movies and images can be in a single folder.

The postfix of each artwork type can be specified in the settings section of the the add-on.

For example:
clearlogo = "-clearlogo.jpg" instead of "-logo.png"

Has been tested on Windows and Raspberry Pi 3 with OSMC.

# To be done
- Error handling, e.g adding .xyz as an extension in settings will not be handled properly
- Adding artwork for other media than just movies 
- There can be only one image file type per artwork type, e.g. all logos are png or jpg, but there can be no mix of them