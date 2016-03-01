flickr_headers (and profile color)
==============
Use a random image from a Flickr search as your Twitter header (example searches a tag)

This branch finds the dominant color from the image and uses it to update your profile color. 


Requirements
------------
  - tweepy  `pip install tweepy`
  - flickrapi `pip install flickrapi`
  
Notes
-----
  - Just add your keys to flickr_headers_keys.py
  - color sampling and k-means clustering based on <a href="http://charlesleifer.com/blog/using-python-and-k-means-to-find-the-dominant-colors-in-images/">this post</a> by Charles Leifer.
  
  
