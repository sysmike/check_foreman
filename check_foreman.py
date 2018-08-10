#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import sys
import json
import ssl
from time import sleep
from argparse import ArgumentParser

parser = ArgumentParser(add_help=False)
parser.add_argument('-H', '--hostname', dest='hostname', metavar='ADDRESS', required=True, help="host name or IP address")
parser.add_argument('-U', '--user', dest='username', metavar='USERNAME', required=True, help="foreman username")
parser.add_argument('-P', '--password', dest='password', metavar='PASSWORD', required=True, help="foreman password")
args = parser.parse_args()

def get_stats():

    global total_hosts

    tries = 5

    while tries >= 0:
        try:
            url = 'https://{}/api/dashboard'.format(hostname)
            headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0' }
            req = urllib2.Request(url, None, headers)
            html = urlopen(req)
            data = json.loads(html.read())
            if data:
                total_hosts = data['data']['total_hosts']
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

    get_stats()

    print('Your mining rigs are running at ' + str(hashrate) + 'MH/s and you are making ' + str(usdpermin) + '$ a day | '
            + 'reported_hashrate=' + str(reported_hashrate) + ' averagehashrate=' + str(averagehashrate) + ' hashrate=' + 
str(hashrate)
            + ' validshares=' + str(validshares) + ' invalidshares=' + str(invalidshares) + ' staleshares=' + str(staleshares)
            + ' active_workers=' + str(active_workers) + ' unpaid=' + str(unpaid))

    if averagehashrate < 50:
        sys.exit(2)
    else:
        sys.exit(0)

except Exception as e:

    print e
    sys.exit(1)
