#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
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
    global bad_hosts
    global active_hosts
    global ok_hosts
    global out_of_sync_hosts
    global disabled_hosts
    global reports_missing
    global percentage

    tries = 5

    while tries >= 0:
        try:

            url = 'https://{}/api/dashboard'.format(str(args.hostname))
            r = requests.get(url, auth=(str(args.username), str(args.password)))
            data = r.json()
            print(data)
            if data:
                total_hosts = data['total_hosts']
                bad_hosts = data['bad_hosts']
                active_hosts = data['active_hosts']
                ok_hosts = data['ok_hosts']
                out_of_sync_hosts = data['out_of_sync_hosts']
                disabled_hosts = data['disabled_hosts']
                reports_missing = data['reports_missing']
                percentage = data['percentage']
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

    graphite = ' | ' + 'total_hosts=' + str(total_hosts) + ' bad_hosts=' + str(bad_hosts) + ' active_hosts=' + str(active_hosts)
            + ' ok_hosts=' + str(ok_hosts) + ' out_of_sync_hosts=' + str(out_of_sync_hosts) + ' disabled_hosts=' + str(disabled_hosts)
            + ' reports_missing=' + str(reports_missing) + ' percentage=' + str(percentage)

    if bad_hosts > 1 :
        print()
        sys.exit(2)
    elif out_of_sync_hosts > 1 :
        print()
        sys.exit(1)
    else:
        print()
        sys.exit(0)

except Exception as e:

    print (e)
    sys.exit(1)
