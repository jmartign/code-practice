#/usr/bin/env python
# -*- encoding: utf-8 -*-
import time
import redis

r = redis.StrictRedis(host='localhost', port=6379)
ps = r.pubsub()
ps.subscribe('channel-1')
msg = ps.get_message()
print 'subscribed', msg['data']

count = 0
#while count < 10:
#    msg = ps.get_message()
#    if msg:
#        print 'received msg:', msg['data']
#        count += 1
#    time.sleep(0.01)
for message in ps.listen():
    print 'received msg:', message['data']
    count += 1
    if count >= 10:
        break
ps.close()
print 'closed'

