#!/usr/bin/python

# Simple Flickr folder uploader
# Author: Alfonso E.M. <alfonso@el-magnifico.org>
# Inspired in https://github.com/sybrenstuvel/flickrapi and https://github.com/jamesmstone/flickr-uploadr

# Get an api key and an api secret: https://www.flickr.com/services/apps/create/apply
# Put those values in these variables

API_KEY = "paste-your-api-key-here"
API_SECRET = "paste-your-api-secret-here"

# Start this script. First time it shows an URL. Open it with your browser and authorize the script.

# Once authorized, script will store a token in user home directory. Change it if desired:
#TOKEN_CACHE='./token'

import flickrapi
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("folder", help="Path to the folder you want to upload")
parser.add_argument("-t", "--tags", help="One or more tags for all the files (use quotes if needed)")
parser.add_argument("-n", "--name", help="Name of the set (use quotes if needed)")
params=parser.parse_args()


FOLDER=os.path.abspath(params.folder)+"/"

if params.name:
  TITLE=params.name
else:
  TITLE=os.path.basename(os.path.normpath(params.folder))
if params.tags:
  TAGS=params.tags
else: 
  TAGS="synology-nas-uploaded"

print "Uploading", FOLDER, "to", TITLE, "with tags:", TAGS


flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, token_cache_location=TOKEN_CACHE)

if not flickr.token_valid(perms='write'):
    print "Authentication required"

    # Get request token
    flickr.get_request_token(oauth_callback='oob')

    # Show url. Copy and paste it in your browser
    authorize_url = flickr.auth_url(perms=u'write')
    print(authorize_url)

    # Prompt for verifier code from the user 
    verifier = unicode(raw_input('Verifier code: '))

    print "Verifier:", verifier

    # Trade the request token for an access token
    print(flickr.get_access_token(verifier))


params = {}
params['tags']=TAGS
photo_ids=[]

for filename in os.listdir(FOLDER):
    filename_split = filename.split('.')

    if len(filename_split) == 2:
        ext = filename_split[1].lower()
    else:
        ext = ''
    if ext in ['png', 'jpeg', 'jpg', 'avi', 'mp4', 'gif', 'tiff', 'mov', 'wmv', 'ogv', 'mpg', 'mp2', 'mpeg',
               'mpe', 'mpv']:

        print(filename),
        full_filename = FOLDER + filename

        try:
            uploadResp = flickr.upload(filename=full_filename, is_public=0, is_friend=0, is_family=1, tags=TAGS)
            photo_id = uploadResp.findall('photoid')[0].text
            print(' OK. Flickr id = ' + photo_id)
            photo_ids.append(photo_id)
        except:
            print(" ERROR.")

# Creating a set
try:
    print "Creating set",TITLE,
    resp = flickr.photosets.create(title=TITLE,primary_photo_id=photo_ids[0])
    photoset_id = photoset_id = resp.findall('photoset')[0].attrib['id']
    print(' OK. Set id = ' + photoset_id)
    del photo_ids[0]
except:
    print "ERROR."
    sys.exit(4)

for photo_id in photo_ids:
    try:
        resp = flickr.photosets.addPhoto(photoset_id=photoset_id,photo_id=photo_id)
    except:
        print "ERROR adding file to set", photo_id


