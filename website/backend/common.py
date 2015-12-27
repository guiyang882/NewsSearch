#!/usr/bin/env python
# coding=utf-8
import sys
import os
sys.path.append(os.path.realpath(".."))
import traceback
import time
import web
import bson
from bson.json_util import dumps
from utils import *
import conf
import re
import hashlib
import json
from database.redisclient import redis

sys.path.append("../")


FILTERS = {
    'strategy_id': lambda _: bson.objectid.ObjectId(_),
    'uid': re.compile(r'[-_a-zA-Z0-9\.]{1,63}$'),
    'email': re.compile(r'^[^@]+@[^@]+\.[^@]+$'),
    'datetime': lambda _: _ and int(_) or None,
    'objectid': lambda _: bson.objectid.ObjectId(_),
    'positive_integer': lambda _: int(_) >= 0,
    'md5': re.compile(r'^[a-fA-F0-9]{32}$'),
    'country_code': re.compile(r'^[a-zA-Z]{2}$'),
    'uuid': re.compile(r'^[-a-fA-F0-9]+$'),
    'base64': re.compile(r'^[a-zA-Z0-9+/=]+$'),
    'int': re.compile(r'^\d+$'),
    'float': re.compile(r'^\d+\.?\d*$'),
    'bool': lambda _: _.lower() in ('true','false'),
    'date': re.compile(r'^\d{4}-\d{2}-\d{2}$')
}

def result(status, message, data = None):
    bjson_to_plaintext(data)
    ret = {"status": status, "message": message, "data": data, "timestamp": int(time.time())} 
    return dumps(ret) 

def set_header():
    if conf.test:
        web.header('Access-Control-Allow-Origin','*')
    web.header("Content-Type", "application/json")
    web.header("Cache-Control", "no-cache, no-store, max-age=0, must-revalidate")

def gen_token(u):
    token = hashlib.sha256(json.dumps({
        'uid': u.get('username'), 
        'pass': u.get('password'),
        'key': "Pi8VhsV8Pm",
        'timestamp': int(time.time())
    }, encoding='latin1')).hexdigest()[::2]
    return token 

def set_token(u):
       
    token = web.cookies().get(conf.session_name)

    if u is None:
        web.setcookie('username', '', 0, path="/")
        web.setcookie('gpxtoken', '', 0, path="/")
        if token:
            redis.delete('token:' + token)
        return

    if token is None:
        token = gen_token(u)

    try:
        u['token'] = token 
        redis.setex('token:' + token, conf.session_timeout, json.dumps({"username":u['username'], "_id": str(u["_id"])}))
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        tbs = ''.join(traceback.format_exception(exc_type, exc_obj, exc_tb))
        print tbs

    web.setcookie('username', u['username'], conf.session_timeout, path="/")
    web.setcookie('gpxtoken', token, conf.session_timeout, path="/")

    return token 

def validate_user():
    token = web.cookies().get(conf.session_name)
    if token:
        user = redis.get("token:" + token)
        if user:
            redis.expire("token:" + token, conf.session_timeout)
            return json.loads(user)
    return 

if __name__ == '__main__':
    print result(0, "success", {"test":123,"ssss":"ssdfd"})
    print gen_token({"username":"aaa","password":"sss"})
