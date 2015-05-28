import socket
import struct
import hashlib
import base64
import threading,random
 
# Accept WebSocket version 13

connectionlist = {}
 
def sendMessage(message):
    global connectionlist
    for connection in connectionlist.values():
        connection.send("\x00%s\xFF" % message)
 
def deleteconnection(item):
    global connectionlist
    del connectionlist['connection'+item]
     
class WebSocket(threading.Thread):
    def __init__(self,conn,index,name,remote, path="/"):
        threading.Thread.__init__(self)
        self.conn = conn
        self.index = index
        self.name = name
        self.remote = remote
        self.path = path
        self.buffer = ""
         
    def run(self):
        print 'Socket%s Start!' % self.index
        headers = {}
        self.handshaken = False
 
        while True:
            if self.handshaken == False:
                print 'Socket%s Start Handshaken with %s!' % (self.index,self.remote)
                self.buffer += self.conn.recv(1024)
                if self.buffer.find('\r\n\r\n') != -1:
                    header, data = self.buffer.split('\r\n\r\n', 1)
                    for line in header.split("\r\n")[1:]:
                        key, value = line.split(": ", 1)
                        headers[key] = value
 
                    headers["Location"] = "ws://%s%s" %(headers["Host"], self.path)
                    key = headers['Sec-WebSocket-Key']
                    sha = hashlib.sha1()
                    sha.update(key)
                    sha.update('258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
                    ak = base64.b64encode(sha.digest())
                     
                    handshake = '\
HTTP/1.1 101 Switching Protocols\r\n\
Upgrade: websocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Accept: %s\r\n\
Sec-WebSocket-Origin: %s\r\n\
Sec-WebSocket-Location: %s\r\n\r\n\
' %(ak, headers['Origin'], headers['Location'])
 
 
                    self.conn.send(handshake)
                    self.handshaken = True
                    print 'Socket%s Handshaken with %s success!' % (self.index,self.remote)
                    sendMessage('Welcome, '+self.name+' !')
            else:
                self.buffer += self.conn.recv(64)
                if self.buffer.find("\xFF")!=-1:
                    s = self.buffer.split("\xFF")[0][1:]
                    if s=='quit':
                        print 'Socket%s Logout!' % (self.index)
                        sendMessage(self.name+' Logout')
                        deleteconnection(str(self.index))
                        self.conn.close()
                        break
                    else:
                        print 'Socket%s Got msg:%s from %s!' % (self.index,s,self.remote)
                        sendMessage(self.name+':'+s)
                    self.buffer = ""
     
 
class WebSocketServer(object):
    def __init__(self):
        self.socket = None
    def begin(self):
        print 'WebSocketServer Start!'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("127.0.0.1",1234))
        self.socket.listen(50)
         
        global connectionlist
         
        i=0
        while True:
            connection, address = self.socket.accept()
             
            username=address[0]
             
            newSocket = WebSocket(connection,i,username,address)
            newSocket.start()
            connectionlist['connection'+str(i)]=connection
            i = i + 1
 
if __name__ == "__main__":
    server = WebSocketServer()
    server.begin()

