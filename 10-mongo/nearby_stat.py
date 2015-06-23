#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import json
import pymongo
from bson.son import SON

mongo_client = pymongo.MongoClient('127.0.0.1', 27017)

DB_NAME = 'himomo'
COLLECTION_NAME = 'nearby2'


def count_sex():
    db = mongo_client[DB_NAME]
    pipeline = [
        {'$group': {'_id': '$sex', 'total': {'$sum': 1},
                    'min_distance': {'$min': '$distance'},
                    'max_distance': {'$max': '$distance'}
        }},
        {'$sort': SON([('total', -1)])}
    ]
    l = list(db[COLLECTION_NAME].aggregate(pipeline))
    total = l[0]['total'] + l[1]['total']
    max_distance = '{:.2f}km'.format(max(l[0]['max_distance'], l[1]['max_distance'])/1000)
    min_distance = '{:.2f}km'.format(min(l[0]['min_distance'], l[1]['min_distance'])/1000)
    data = {l[0]['_id']: l[0]['total'], l[1]['_id']: l[1]['total']}
    return {
        'total': total,
        'max_distance': max_distance,
        'min_distance': min_distance,
        'data': data
    }


def count_age():
    db = mongo_client[DB_NAME]
    pipeline = [
        {'$group':{
            '_id': {'age': '$age', 'sex': '$sex'},
            'total': {'$sum': 1}
        }},
        {'$project':{
            '_id': 0,
            'age': '$_id.age',
            'sex': '$_id.sex',
            'total': 1
        }}
    ]
    sex_age = {'F': {}, 'M': {}}
    l = list(db[COLLECTION_NAME].aggregate(pipeline))
    for d in l:
        sex_age[d['sex']][d['age']] = d['total']
    ages = list(set(sex_age['F'].keys()) | set(sex_age['M'].keys()))
    data = {
        'F': [sex_age['F'].get(n, 0) for n in ages],
        'M': [sex_age['M'].get(n, 0) for n in ages],
    }
    return {
        'ages': ages,
        'data': data
    }


def count_vip():
    db = mongo_client[DB_NAME]
    pipeline = [
        {'$group':{
            '_id': {'sex': '$sex', 'vip': '$vip_level'},
            'total': {'$sum': 1}
        }},
        {'$project': {
            '_id': 0,
            'sex': '$_id.sex',
            'vip': '$_id.vip',
            'total': 1
        }}
    ]
    sex_vip = {'F': {}, 'M': {}}
    l = list(db[COLLECTION_NAME].aggregate(pipeline))
    for d in l:
        sex_vip[d['sex']]['VIP' + str(d['vip'])] = d['total']
    return sex_vip


def count_client():
    db = mongo_client[DB_NAME]
    pipeline = [
        {'$group':{
            '_id': {'sex': '$sex', 'client': '$client'},
            'total': {'$sum': 1}
        }},
        {'$project': {
            '_id': 0,
            'sex': '$_id.sex',
            'client': '$_id.client',
            'total': 1
        }}
    ]
    sex_client = {'F': {}, 'M': {}}
    l = list(db[COLLECTION_NAME].aggregate(pipeline))
    for d in l:
        sex = d['sex']
        m_client = d['client']
        count = d['total']
        if '/' in m_client:
            i = m_client.find('/')
            m_client = m_client[:i]
        n = sex_client[sex].get(m_client, 0)
        sex_client[sex][m_client] = n + count
    return sex_client

resp = {
    'chart-1': count_sex(),
    'chart-2': count_age(),
    'chart-3': count_vip(),
    'chart-4': count_client()
}

fp = open('nearby_stat.json', 'w')
json.dump(resp, fp)
fp.close()

