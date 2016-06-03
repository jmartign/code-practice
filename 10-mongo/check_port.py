#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import sys
import socket

CLIENT_PORT = 27017
WEB_PORT = 28017

socket.setdefaulttimeout(1)

def check_port_opened(host, port):
    try:
        socket.create_connection((host, port), 0.5)
        return True
    except socket.timeout:
        pass
    except Exception as ex:
        raise ex
    return False


def check_for_host(host):
    client_port_opened = check_port_opened(host, CLIENT_PORT)
    web_port_opened = check_port_opened(host, WEB_PORT)
    auth_enabled = False

    if client_port_opened:
        import pymongo
        try:
            pymongo.MongoClient(host, CLIENT_PORT).database_names()
        except pymongo.errors.OperationFailure as ex:
            # print dir(ex)
            if ex.message == 'unauthorized':
                auth_enabled = True
        except pymongo.errors.ServerSelectionTimeoutError:
            client_port_opened = False
    print('== Checked host %s' % host)
    print('  Mongo client port %d is %s, auth is %s' % (CLIENT_PORT, 
            (client_port_opened and 'OPEN' or 'CLOSE'), 
            (auth_enabled and 'ENABLED' or 'DISABLED')))
    print('  web port %d is %s' % (WEB_PORT, (web_port_opened and 'OPEN' or 'CLOSE')))


if __name__ == '__main__':
    host = '127.0.0.1'
    if len(sys.argv) == 1:
        check_for_host(host)
        
        host = socket.gethostbyname(socket.gethostname())
        check_for_host(host)
    else:
        host = sys.argv[1]
        check_for_host(host)
