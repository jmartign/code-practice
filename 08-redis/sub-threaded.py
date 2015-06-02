#/usr/bin/env python
# -*- encoding: utf-8 -*-
import time
import redis

def msg_handler(msg):
    print 'received-msg', msg['data']

r = redis.StrictRedis(host='localhost', port=6380)
ps = r.pubsub(ignore_subscribe_messages=True)
ps.subscribe(**{'channel-1':msg_handler})

thd = ps.run_in_thread(sleep_time=0.001)

time.sleep(10)
thd.stop()
ps.close()

print 'closed'

