#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, hashlib, zlib
import pyrebase
import webbrowser

config = {
  "apiKey": "AIzaSyB92upOPgf8HcF3QZ_xhz39cN3OsWKKBrs",
  "authDomain": "p-sync.firebaseapp.com",
  "databaseURL": "https://psync-ufcg.firebaseio.com",
  "storageBucket": "psync-ufcg.appspot.com",
  "serviceAccount": "./serviceAccountKey.json"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
webbrowser.open('https://github.com/login/oauth/authorize?client_id=1017b4f61c8abdd18c16', new=2)

def write_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)

def init(repo):
    os.mkdir(repo)
    os.mkdir(os.path.join(repo, '.psync'))
    for name in ['objects', 'refs', 'refs/heads']:
        os.mkdir(os.path.join(repo, '.psync', name))
    write_file(os.path.join(repo, '.psync', 'HEAD'),
               b'ref: refs/heads/master')
    print('initialized empty psync repository: {}'.format(repo))


def hash_object(data, obj_type, write=True):
    header = '{} {}'.format(obj_type, len(data)).encode()
    full_data = header + b'\x00' + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    if write:
        path = os.path.join('.psync', 'objects', sha1[:2], sha1[2:])
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            write_file(path, zlib.compress(full_data))
    return sha1