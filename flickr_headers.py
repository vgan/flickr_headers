#!/usr/bin/env python
import flickrapi
import tweepy
from random import randint
import random
import os
import urllib
from flickr_headers_keys import *
from collections import namedtuple
from math import sqrt
try:
    import Image
except ImportError:
    from PIL import Image

flickr = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET)
auth = tweepy.OAuthHandler(TWITTER_API_KEY,TWITTER_API_SECRET)
auth.set_access_token(TWITTER_TOKEN,TWITTER_TOKEN_SECRET)
api = tweepy.API(auth)

photos = flickr.photos.search(tags="stevecvardotcom",format="parsed-json",per_page="500")
image = 'header.jpg'
total = int(photos['photos']['total'])
photosize = 'c' # b is 1024 on long side -  see: http://www.flickr.com/services/api/misc.urls.html 
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

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

filename = image
def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '%s' % ''.join(('%02x' % p for p in rgb))

def colorz(filename, n=3):
    img = Image.open(filename)
    img.thumbnail((200, 200))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)

def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters

test = colorz(filename,1)

profile_link_color = test[0]

if os.path.isfile(image):
        try:
                update_header = api.update_profile_banner(filename=image)
		update_color = api.update_profile(profile_link_color=profile_link_color)
                os.remove(image)
        except:
                print 'couldnt update header'
