#!/usr/bin/env python
# -*- coding: utf-8 -*-

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