#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import ssl
from time import sleep
from argparse import ArgumentParser
try:
    import requests
except ImportError:
    print("Please install the python-requests module.")
    sys.exit(-1)

parser = ArgumentParser(add_help=False)
parser.add_argument('-H', '--hostname', dest='hostname', metavar='ADDRESS', required=True, help="host name or IP address")
parser.add_argument('-U', '--user', dest='username', metavar='USERNAME', required=True, help="foreman username")
parser.add_argument('-P', '--password', dest='password', metavar='PASSWORD', required=True, help="foreman password")
args = parser.parse_args()

def results():

    global total_hosts

    tries = 5

    while tries >= 0:
        try:

            url = 'https://{}/api/dashboard'.format(str(args.hostname))
            r = requests.get(url, auth=(str(args.username), str(args.password)))
            data = r.json()
            print(data)
            if data:
                total_hosts = data['total_hosts']
                break
            else:
                sleep(15)
        except:
            if tries == 0:
                raise
            else:
                sleep(10)
                tries -= 1
                continue

try:

    results()

    print()

    if averagehashrate > 1 :
        sys.exit(2)
    else:
        sys.exit(0)

except Exception as e:

    print (e)
    sys.exit(1)
