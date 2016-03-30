# Script.artwork.loader

This Kodi addon will add local artwork to the Kodi database **for movies only**.

It can add the following artwork types:
- clearlogo
- clearart
- banner
- discart

Kodi itself cannot add these artwork types to the database at the time of writing (Kodi 16.1 or earlier). It **can** add poster and fanart via the nfo file, but not e.g. a clearlogo.

Compared to the "artwork downloader" addon: that one downloads files from e.g. fanart.tv, but has no option to load "sidecar" images from disk.

This addon expects the artwork files to be "sidecar" files, so in the same folder as the movie and named like this:

- c:\movies\a.mp4
- c:\movies\a-logo.png

or
- //there/are/movies/here/movie1.mkv
- //there/are/movies/here/movie1-art.png

This is different from the "artwork downloader", which can load local files, but expects each movie to be in its own folder with a generic "logo.png" file. 

The "artwork loader" expects each image to be named after the movie and in the same folder as the movie, but all movies and images can be in a single folder.

## Settings

In settings you can specify which artwork type should be added by enabling or disabling it.

The postfix of each artwork type can be specified in the settings section of the the add-on.

For example:
clearlogo = "-clearlogo.jpg" instead of "-logo.png"

This addon also gives you the possibility to create your own second-rate clearlogos, because getting an image approved on e.g. fanart.tv can be cumbersome because of the high level of quality they expect.

It is also possible to use the same image for multiple artworks.

For example, specify this in settings to use the logo for both clearlogo and clearart:

- clearlogo = "-logo.png" 
- clearart = "-logo.png"

## Installation

1. Click Download ZIP in the top-right corner on github
2. Copy the contents of the master.zip file including the foldername **script.artwork.loader** to:
  - OSMC from Windows SMB: \\\\**ipadres**\\osmc\\.kodi\\addons
  - OSMC using SFTP: \\\\**ipadres**\\osmc\\.kodi\\addons
  - Windows: **windows root drive**:\\Users\\**username**\\appData\\Roaming\\Kodi\\addons

And restart Kodi.

Or use the Kodi interface to add an addon from zip file.

## Inner workings

The addon works like this:
- Get a list of all movies in the Kodi database using the JSON-RPC API
- For each movie, check which artwork types should be added, as configured in settings. If none are specified, the addon exits
  - For each artwork type, check if that artwork file exists on disk next to the movie:
    - if it does, overwrite existing artwork entry in the database using the JSON-RPC API and refresh the thumbnail cache for this image
    - if it doesn't, check next artwork type
    - if all artwork types have been checked for the movie, goto next movie on the list
- Quit if all movies have been parsed

If the disk is unavailable, e.g. an external drive with the movies is not attached, it will not find any artwork and not add anything to the Kodi database.

## Testing

Has been tested on Windows and Raspberry Pi 3 with OSMC.

## To be done
- Error handling, e.g adding .xyz as an extension in settings, which would load a non-image file, will not be handled properly
- Adding artwork for other media than just movies 
- There can be only one image file type per artwork type, e.g. all logos are png or jpg, but there can be no mix of them

## Acknowledgements

Most of the code in the lib folder is a shameless rip from the script.artwork.downloader addon by **Martijn Kaijser**. However, only two or three functions from his code are used and I've already removed a lot of code from it which is not needed by this addon.