#!/usr/bin/env python
import flickrapi
import tweepy
from random import randint
import os
import urllib
from flickr_headers_keys import *

flickr = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET)
auth = tweepy.OAuthHandler(TWITTER_API_KEY,TWITTER_API_SECRET)
auth.set_access_token(TWITTER_TOKEN,TWITTER_TOKEN_SECRET)
api = tweepy.API(auth)

photos = flickr.photos.search(tags="stevecvardotcom",format="parsed-json",per_page="500")
image = 'header.jpg'
total = int(photos['photos']['total'])
photosize = 'b' # b is 1024 on long side -  see: http://www.flickr.com/services/api/misc.urls.html 
rando = randint(0, (total -1))

photoid = str(photos['photos']['photo'][rando]['id'])
photofarm = str(photos['photos']['photo'][rando]['farm'])
photoserver = str(photos['photos']['photo'][rando]['server'])
photosecret = str(photos['photos']['photo'][rando]['secret'])

photoURL = 'http://farm' + photofarm + '.static.flickr.com/' + photoserver + '/' + photoid + '_' + photosecret + '_' + photosize + '.jpg'

try:
	urllib.urlretrieve(photoURL,image)
except:
	print 'couldnt download image from flickr: ' + photoURL

if os.path.isfile(image):
	try:
		update_header = api.update_profile_banner(filename=image)
		os.remove(image)
	except:
		print 'couldnt update header'
