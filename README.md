# synology-flickr-folder-uploader
Simple script to upload a folder of photos/videos to a new set in Flickr

I have used several scripts to upload photos from my Synology NAS to Flickr, but recently all of them failed (due to a change in authentication api).


So I cooked my own script, based in the work of  https://github.com/sybrenstuvel/flickrapi and https://github.com/jamesmstone
/flickr-uploadr

# Installation 

I have tested these steps in my DS212j. This procedure probably work in many other models.

* Connect via SSH to your Synology NAS
  ssh admin@mynas
* Create a folder for the flickr api
  mkdir api
* Set python to use that folder
  export PYTHONPATH=/var/services/homes/admin/api
* Install the flickr api
  easy_install  --install-dir=/var/services/homes/admin/api flickrapi
* Download the script
  wget
* Edit the script and adjust the paths at the begining
* Give it execution permissions
  chmod u+x flickr-folder-uploader.py
* Run it!
  ./flickr-folder-uploader.py /volume1/alfem/Pics/Coches/ coches
  First parameter=Folder to upload
  Second parameter=Tag for the photos 
  
You can install the api system wide and avoid setting the PYTHONPATH, but I prefer to keep my NAS system clean.

