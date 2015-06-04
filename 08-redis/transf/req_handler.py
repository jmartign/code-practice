#/usr/bin/env python
# -*- encoding: utf-8 -*-
import time
import json
import redis
import pymongo, gridfs, bson
import requests
import urllib2
import tempfile

REDIS_CHANNEL = 'momo.img'

mongo_client = pymongo.MongoClient('localhost', 27017)
mongo_db = mongo_client['momo_img']
mongo_db_gfs = gridfs.GridFS(mongo_db, collection='fs')

def download_img(imgid):
    img_url = 'xxx'
    req = urllib2.Request(img_url)
    conn = urllib2.urlopen(req)
    f = tempfile.TemporaryFile()
    f.write(conn.read())
    return f

def store_img(imgid):
    global mongo_db_gfs
    f = download_img(imgid)
    gfs_id = mongo_db_gfs.put(f, filename=imgid)
    return gfs_id

def msg_handler(msg):
    data = json.loads(msg['data'])
    gfs_id = store_img(data['imgid'])
    data['gfs_id'] = gfs_id
    mongo_db.insert(data)

redis_client = redis.StrictRedis(host='localhost', port=6380)
ps = redis_client.pubsub(ignore_subscribe_messages=True)
ps.subscribe(**{REDIS_CHANNEL:msg_handler})

thd = ps.run_in_thread(sleep_time=0.01)

thd.join()

print 'closed'


