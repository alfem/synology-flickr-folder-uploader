#!/usr/bin/python

# Simple Flickr folder uploader
# Author: Alfonso E.M. <alfonso@el-magnifico.org>
# Inspired in https://github.com/sybrenstuvel/flickrapi and https://github.com/jamesmstone/flickr-uploadr

# Get an api key and an api secret: https://www.flickr.com/services/apps/create/apply
# Put those values in these variables
import flickrapi
import os
import sys
import argparse
import re

API_KEY = "paste-your-api-key-here"
API_SECRET = "paste-your-api-secret-here"
USER_ID = "paste-your-user-id-here"

# Start this script. First time it shows an URL. Open it with your browser and authorize the script.

# Once authorized, script will store a token in user home directory. Change it if desired:
TOKEN_CACHE = './token'


def parse_input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Path to the folder you want to upload")
    parser.add_argument("-t", "--tags", help="One or more tags for all the files (use quotes if needed)")
    parser.add_argument("-n", "--name", help="Name of the set (use quotes if needed)")
    params = parser.parse_args()

    folder = os.path.abspath(params.folder) + "/"

    if params.name:
        title = params.name
    else:
        title = os.path.basename(os.path.normpath(params.folder))
    if params.tags:
        tags = params.tags
    else:
        tags = "synology-nas-uploaded"

    print "Uploading", folder, "to", title, "with tags:", tags
    return {'folder': folder, 'title': title, 'tags': tags}


def create_set(name, primary_photo_id):
    try:
        print "Creating set.", name,
        resp = flickr.photosets.create(title=name, primary_photo_id=primary_photo_id)
        photoset_id = resp.find('photoset').attrib['id']
        print 'OK. Set id = ', photoset_id
        return photoset_id
    except:
        print "ERROR."
        sys.exit(4)


def find_set(name, user_id):
    try:
        print "Looking for set.", name,
        sets_response = flickr.photosets.getList(user_id=user_id)
        photo_sets = sets_response.find('photosets').findall('photoset')
        for photo_set in photo_sets:
            if name == photo_set.find('title').text:
                print "Found."
                return photo_set.get('id')
        print "Doesn't exist."
        return None
    except:
        print "ERROR."


def check_authentication():
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
        print flickr.get_access_token(verifier)


def upload_photos(folder):
    photo_ids = []
    pattern = re.compile('\.([a-zA-Z]+)$')

    for filename in os.listdir(folder):
        ext = pattern.search(filename)
        if ext:
            ext = ext.group(1).lower()

            if ext in ['png', 'jpeg', 'jpg', 'avi', 'mp4', 'gif', 'tiff', 'mov', 'wmv', 'ogv', 'mpg', 'mp2', 'mpeg',
                       'mpe', 'mpv']:

                print filename,
                full_filename = folder + filename

                try:
                    uploadResp = flickr.upload(filename=full_filename, is_public=0, is_friend=1, is_family=1,
                                               tags=input_args['tags'])
                    photo_id = uploadResp.find('photoid').text
                    print " OK. Flickr id = ", photo_id
                    photo_ids.append(photo_id)
                except:
                    print " ERROR."
    print len(photo_ids), "photos uploaded successfully"
    return photo_ids


def add_photos_to_set(photo_ids, set_id):
    if set_id is None:
        return
    for photo_id in photo_ids:
        try:
            flickr.photosets.addPhoto(photoset_id=set_id, photo_id=photo_id)
        except:
            print "ERROR adding file to set", photo_id


input_args = parse_input_args()
flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, token_cache_location=TOKEN_CACHE)
check_authentication()
photo_ids = upload_photos(folder=input_args['folder'])
photoset_id = find_set(name=input_args['title'], user_id=USER_ID)

if photoset_id is None and len(photo_ids) != 0:
    photoset_id = create_set(name=input_args['title'], primary_photo_id=photo_ids[0])
    del photo_ids[0]

add_photos_to_set(photo_ids, photoset_id)
