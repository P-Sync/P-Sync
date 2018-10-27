#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psync
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
    
    args = parser.parse_args()
    
    if args.command == 'init':
        psync.init(args.repo)
    elif args.command == 'status':
        psync.status()
    else:
        assert False, 'unexpected command {!r}'.format(args.command)
if __name__ == '__main__':
    main()