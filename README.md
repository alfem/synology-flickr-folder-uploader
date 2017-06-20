# synology-flickr-folder-uploader
Simple script to upload a folder of photos/videos to a new set in Flickr

I have used several scripts to upload photos from my Synology NAS to Flickr, but recently all of them failed (due to a change in authentication api).


So I cooked my own script, based in the work of  https://github.com/sybrenstuvel/flickrapi and https://github.com/jamesmstone
/flickr-uploadr

# Installation 

I have tested these steps in my DS212j, but this procedure probably work in many other models.

* Connect via SSH to your Synology NAS

  ssh admin@mynas

* Create a folder for the flickr api

  mkdir api

* Set python to use that folder

  export PYTHONPATH=/var/services/homes/admin/api

* Install the flickr api

  easy_install  --install-dir=/var/services/homes/admin/api flickrapi

* Download the script (use your favourite browser, or wget command in your Synology)

  wget https://raw.githubusercontent.com/alfem/synology-flickr-folder-uploader/master/flickr-folder-uploader.py
 
* Give it execution permissions

  chmod u+x flickr-folder-uploader.py

* Create a new app in your Flickr account: https://www.flickr.com/services/apps/create/apply and jot down api_key and api_secret
* Edit the script and adjust the api_key, api_secreet and paths at the begining
* Run it!

  ./flickr-folder-uploader.py /volume1/alfem/Pics/Coches/ coches

  First parameter = Folder to upload
  
  Second parameter = Tag for the photos 

* On first run, the script will show an URL you need to visit in order to authorize it.Open the url in your brwoser, authorize the script and copy the code shown.   

You can install the api system wide and avoid setting the PYTHONPATH, but I prefer to keep my NAS system clean.

