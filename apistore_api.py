# coding=utf-8
import requests
import json
import codecs



# http://apistore.baidu.com/astore/serviceinfo/1840.html
def get_ip_address(ip):
    params = {'ip': ip}
    resp = requests.get('http://apistore.baidu.com/microservice/iplookup', params=params)
    return resp.json()

def get_mobile_num(mobile_num):
    params = {'tel': mobile_num}
    resp = requests.get('http://apistore.baidu.com/microservice/mobilephone', params=params)
    return resp.json()

def query_id(query_param):
    def output_msg(msg):
        f = codecs.open('apistore.txt', 'w', 'utf-8')
        f.write(msg)
        f.close()

    #ret_data = get_ip_address(query_param)
    ret_data = get_mobile_num(query_param)
    if ret_data['errNum'] == 0:
        output_msg(json.dumps(ret_data['retData']))
    elif ret_data['errMsg'] == 'success':
        output_msg(ret_data['retData'][0])
    else:
        output_msg(ret_data['errMsg'])
#query_id('117.89.35.58')
query_id('15846530170')

