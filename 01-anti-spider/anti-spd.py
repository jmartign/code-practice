#!/usr/bin/python

import memcache
import web
render = web.template.render('templates/')

mc = memcache.Client(['localhost:11211'], debug=0)

urls = (
    '/', 'index',
    '/search', 'search',
    '/memcache', 'mem'
)


class index:
  def GET(self):
    return render.index()

  def POST(self):
    data = web.input().get('searchstr')
    srcip = str(web.ctx['ip'])
    print srcip
    if mc.get(srcip):
        mc.incr(srcip)
    else:
      mc.set(srcip, 1)
    if mc.get(srcip) > 3:
      print 'memcache count: ', mc.get(srcip)
      return render.bug()
    else:
      return render.index(data)


class mem:
  def GET(self):
    srcip = str(web.ctx['ip'])
    if mc.get(srcip):
      mc.decr(srcip)

if __name__ == '__main__':
  app = web.application(urls, globals())
  app.run()

