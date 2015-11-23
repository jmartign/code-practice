#-*-coding:utf-8-*- 
from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, redirect

import urllib2
import os
import json
import codecs
import shutil

try:
    import androidhelper as android
except ImportError:
    import android

ASSETS = "/assets/"
ROOT = os.path.dirname(os.path.abspath(__file__))

def _save_from_url(surl, dname):
    jfile = ROOT+'/'+dname
    if not os.path.exists(jfile):
        try:
            data = urllib2.urlopen(surl)
            fd = open(jfile,'w')
            content = data.read()
            fd.write(content)
            data.close()
            fd.close()
        except:
            pass
    else:
        fd = open(jfile)
        content =fd.read()
        fd.close()
        
def _setup_webapp_denps():
    _save_from_url('http://qpython.org/libs/jsonconv.py', 'jsonconv.py')
    _save_from_url('http://qpython.org/libs/ordereddict.py', 'ordereddict.py')

_setup_webapp_denps()


######### QPYTHON WEB SERVER ###############

class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        #sys.stderr.close()
        import threading 
        threading.Thread(target=self.server.shutdown).start() 
        #self.server.shutdown()
        self.server.server_close() 
        print "# QWEBAPPEND"


######### BUILT-IN ROUTERS ###############
def __exit():
    global server
    server.stop()

def __ping():
    return "ok"

def server_static(filepath):
    return static_file(filepath, root=ROOT+'/assets')

PAGE_TEMP = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<meta name="description" content="">
<meta name="author" content="">
<script src="{{assets}}jquery.min.js"></script>
<link href="{{assets}}bootstrap.min.css" rel="stylesheet" />
<script src="{{assets}}bootstrap.min.js"></script>   
<script language='javascript'>
$(document).ready(function(){
%s
});
</script>
<style>
.btn-info { background-color:#ffe052;border-color:#ffe052;color:black}
.placeholder { padding-top:10px;padding-bottom:10px }
.col-xs-6, .col-sm-4 { padding:10px }
ul{ list-style-type: none; margin:0px;padding:0px }
tbody tr th:first-child{ width:80px }
table.nolimit tbody tr th:first-child{ width:auto }
.tt { padding-left:10px; }
.float-right { float:right }
.float-left { float:left }
.center { text-align:center }
.p5 { padding:5px }
.circle {
width: 100%%;
height: 150px;
border-radius: 1px; 
border-color: 1px solid #ddd;
border: solid 1px #ddd;
}
.circle-view {
background-color: #fdfdfd;
}
.circle-text {
padding: 15px 15px 15px 15px;
text-align: center;
font-size:18px;
}
</style>
</head>  
<body>
%s
</body>
</html>
""".replace("{{assets}}",ASSETS)

def home():
    droid = android.Android()
    respond = droid.getLaunchableApplications()
    JS = ""
    CONTENT = u''.join([u'<div>{0}: {1} <a href="/startapp/{1}">Start</a> <a href="/stopapp/{1}">Stop</a></div>'.format(k, v) for k, v in respond.result.items()])
    return template(PAGE_TEMP % (JS, CONTENT))

def startapp(actvy):
    i = actvy.rfind('.')
    if i > 0:
        pkg = actvy[:i]
        droid = android.Android()
        respond = droid.startActivity('android.intent.action.MAIN', packagename=pkg, classname=actvy)
        print respond
    return template(PAGE_TEMP % ('', 'done'))


def stopapp(actvy):
    droid = android.Android()
    i = actvy.rfind('.')
    if i > 0:
        pkg = actvy[:i]
        droid = android.Android()
        respond = droid.forceStopPackage(pkg)
        print respond
    return template(PAGE_TEMP % ('', 'done'))


def download(filepath):
    # /system/app
    print filepath
    shutil.copyfile('/' + filepath, ROOT + '/' + os.path.basename(filepath))
    return template(PAGE_TEMP % ('', 'done'))

def info():
    f = codecs.open(ROOT + '/info.txt', 'wb', 'utf-8')
    f.write('/system/app')
    f.write(u'\n'.join(os.listdir('/system/app')))
    f.write('\n----\n')
    f.write('/system/framework')
    f.write(u'\n'.join(os.listdir('/system/framework')))
    f.close()
    return template(PAGE_TEMP % ('', 'done'))

######### WEBAPP ROUTERS ###############
app = Bottle()
app.route('/', method='GET')(home)
app.route('/__exit', method=['GET','HEAD'])(__exit)
app.route('/__ping', method=['GET','HEAD'])(__ping)
app.route('/assets/:filepath', method='GET')(server_static)

app.route('/startapp/:actvy', method='GET')(startapp)
app.route('/stopapp/:actvy', method='GET')(stopapp)
app.route('/download/<filepath:path>', method='GET')(download)
app.route('/info', method='GET')(info)

try:
    server = MyWSGIRefServer(host="192.168.1.121", port="8080")
    app.run(server=server,reloader=False)
except Exception,ex:
    print "Exception: %s" % repr(ex)

