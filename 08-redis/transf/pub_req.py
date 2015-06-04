#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import redis

REDIS_CHANNEL = 'momo.img'

redis_client = redis.StrictRedis(host='localhost', port=6379)

def publish_msg(msg):
    global redis_client
    redis_client.publish(REDIS_CHANNEL, msg)

msg_data = {
    'id': '123456',
    'catgory': 'feed',
    'momoid': '123456'
    }

publish_msg(json.dumps(msg_data))


