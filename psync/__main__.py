#!/usr/bin/env python
# -*- coding: utf-8 -*-


import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./serviceAccountKey.json')
psync = firebase_admin.initialize_app(cred, name='P-Sync')

db = firestore.client()

def main():
    print('Hello world')
    print(psync.name)
    #TODO

if __name__ == '__main__':
    main()