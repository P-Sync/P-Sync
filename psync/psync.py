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