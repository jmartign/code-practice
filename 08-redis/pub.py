#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time
import redis

r = redis.StrictRedis(host='localhost', port=6379)
for i in range(10):
    r.publish('channel-1', 'hoho message - ' + str(i))
    time.sleep(0.02)

print 'published 10 messages'

