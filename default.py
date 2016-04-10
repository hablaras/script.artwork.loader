#import modules
import os
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import time
import json
from lib.media_setup import _media_listing as media_listing
from traceback import print_exc

THUMBS_CACHE_PATH = xbmc.translatePath( "special://profile/Thumbnails/Video" )

# log to kodi log if log setting is true
def log( txt ):
    if (addon.getSetting("debug_enabled").lower() == "true"):
        if isinstance(txt, unicode):
            txt = txt.encode('utf-8')
        xbmc.log( txt, level=xbmc.LOGNOTICE )
    return

# retrieve cache filename
def get_cached_thumb(filename):
    if filename.startswith("stack://"):
        filename = strPath[ 8 : ].split(" , ")[ 0 ]
    if filename.endswith("folder.jpg"):
        cachedthumb = xbmc.getCacheThumbName(filename)
        thumbpath = os.path.join( THUMBS_CACHE_PATH, cachedthumb[0], cachedthumb ).replace( "/Video" , "")
        # also for Windows!
        thumbpath = thumbpath.replace("\\Video","")
    else:
        cachedthumb = xbmc.getCacheThumbName(filename)
        if ".jpg" in filename:
            cachedthumb = cachedthumb.replace("tbn" ,"jpg")
        elif ".png" in filename:
            cachedthumb = cachedthumb.replace("tbn" ,"png")      
        thumbpath = os.path.join( THUMBS_CACHE_PATH, cachedthumb[0], cachedthumb ).replace( "/Video" , "")
        # also for Windows!
        thumbpath = thumbpath.replace("\\Video","")
    return thumbpath
    
# erase old cache file and copy new one
def erase_current_cache(filename):
    try: 
        cached_thumb = get_cached_thumb(filename)
        log( "File: %s, Cache file: %s" % (filename,cached_thumb) )
        #if xbmcvfs.exists( cached_thumb.replace("png" , "dds").replace("jpg" , "dds") ):
        #    xbmcvfs.delete( cached_thumb.replace("png" , "dds").replace("jpg" , "dds") )
        if xbmcvfs.exists( cached_thumb ):
            xbmcvfs.delete( cached_thumb )
        copy = xbmcvfs.copy( filename , cached_thumb )
        if copy:
            log("Cache succesful")
        else:
            log("Failed to copy to cached thumb")
    except :
        print_exc()
        log("Cache erasing error")

def create_artwork_dict(filename, artwork):
	art = {}
	for k, v in artwork.items():
		basename = ('.').join(filename.split('.')[:-1])
		artname = basename + v
		if (os.path.isfile(artname.encode('utf-8'))):
			art[k] = artname
	return art

# start main routine
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

# xbmcgui.Dialog().ok(addonname, line1, line2, line3)
p = xbmcgui.DialogProgress()
p.create("Start loading movie artwork")
# time.sleep(1)

# artwork to add
artwork = {}
if (addon.getSetting("addclearlogo").lower() == "true"): artwork["clearlogo"] = addon.getSetting("clearlogo")
if (addon.getSetting("addclearart").lower() == "true"): artwork["clearart"] = addon.getSetting("clearart")
if (addon.getSetting("addbanner").lower() == "true"): artwork["banner"] = addon.getSetting("banner")
if (addon.getSetting("adddiscart").lower() == "true"): artwork["discart"] = addon.getSetting("discart")

# EXIT if there is no artwork to add
if ( len(artwork) == 0 ):
	log( "No artwork to add because all settings are false.")
	sys.exit()

p.update(0, str(artwork))
time.sleep(1)

# get list of movies from kodi
mediaList = media_listing("movie") 

itemcount = 0
itemtotal = len(mediaList)

p.update(0, "Parse # of movies: " + str(itemtotal), "Debug: " + addon.getSetting("debug_enabled"))
time.sleep(1) # delays for 1 seconds

locallogo = ""

for item in mediaList:
    itemcount +=1
    p.update(100*itemcount/itemtotal, str(itemcount) + ": " + item['name'] + ", path: " + str(item['path']))
    # create clearlogo filename
    art = create_artwork_dict(item['file'], artwork)
    # at least one type of artwork found locally
    if ( len(art) > 0 ):
        # convert dictionary to string
    	art_json = json.dumps(art).replace("\\","\\\\")
    	p.update(100*itemcount/itemtotal, str(itemcount) + ": " + item['name'] + ", path: " + str(item['path']), "ADD: " + art_json)
	    # add local logo to kodi database
	    #thumb = get_cached_thumb(locallogo)

        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": { "movieid": %i, "art": %s } }, "id": 1 }'%( item['dbid'], art_json ))   
	    # xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": { "movieid": %i, "trailer" : "%s", "art": { "%s": "%s" } }, "id": 1 }'%( item['dbid'], thumb.replace("\\","\\\\"), "clearlogo", locallogo_url ))
	    # refresh kodi thumbnail to be sure a different local logo with the same name gets put in that cache 
        for k,v in art.items():
	    	erase_current_cache(v)
	    # p.update(100*itemcount/itemtotal, "Refreshed thumb: " + thumb)

time.sleep(1) # delays for 1 seconds

p.update(100, "Done!", " ")

time.sleep(1) # delays for 1 seconds
p.close