#!/usr/bin/env python3

import argparse
import requests

def url_parser(target):
    if 'https://' or 'http://' in target:
        if 'https://' in target:
            scheme = 'https://'
            target = target.replace('https://', '')
        if 'http://' in target:
            scheme = 'http://'
            target = target.replace('http://', '')
        else:
            scheme = 'https://'
    url = target.split('/')
    url.insert(0, scheme)
    if url[-1] == '':
        url.pop()
    return url

def find_dirlist(target):
    scode = [400, 401, 403, 404, 500]
    url = target[0] + target[1] + '/'
    for i in range(2, len(target) - 1):
        url = url + target[i] + '/'
        try:
            r = requests.get(url)
        except:
            print('error while requesting URL :(' + url)
            continue
        response = r.text
        if r.status_code not in scode:
            if 'Index of' or 'Directory listing for' in response:
                print(url + ' : Directory listing here')
            else:
                print(url)

parser = argparse.ArgumentParser()
parser.add_argument('--url', '-u', help='Use single url', type=str)
parser.add_argument('--urls', '-U', help='Use multiple urls', type=str)
args = parser.parse_args()

if args.url and args.urls is not None:
    print('Only one argument --url or --urls, -h for help')
    exit()

elif args.url is not None and args.urls is None:
    t = args.url
    url = url_parser(t)
    find_dirlist(url)

elif args.urls is not None and args.url is None:
    try:
        wordlist = args.wordlist
        with open(wordlist) as f:
            lists = f.read().splitlines()
    except:
        print('error in reading ' + wordlist)
        exit()
    for t in lists:
        url = url_parser(t)
        find_dirlist(url)

else:
    print('Only one argument --url or --urls, -h for help')
    exit()
