#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psync, auth_handler
import argparse

def main():
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command', metavar='command')
    sub_parsers.required = True

    sub_parser = sub_parsers.add_parser('init',
            help='initialize a new psync repository')
    sub_parser.add_argument('repo',
            help='directory name for new repository')
    sub_parser = sub_parsers.add_parser('status',
            help='show the working status')
    sub_parser = sub_parsers.add_parser('files',
            help='list files in index')
    sub_parser.add_argument('-s', '--stage', action='store_true',
            help='show object details (mode, hash, and stage number) in '
                 'addition to path')
    sub_parser = sub_parsers.add_parser('add',
            help='add file(s) to index')
    sub_parser.add_argument('paths', nargs='+', metavar='path',
            help='path(s) of files to add')
    sub_parser = sub_parsers.add_parser('login',
        help='login with your google account')

    args = parser.parse_args()
    
    if args.command == 'init':
        psync.init(args.repo)
    elif args.command == 'status':
        psync.status()
    elif args.command == 'files':
        psync.list_files(details=args.stage)
    elif args.command == 'add':
        psync.add(args.paths)
    elif args.command == 'login':
        auth.login()
    else:
        assert False, 'unexpected command {!r}'.format(args.command)
if __name__ == '__main__':
    main()