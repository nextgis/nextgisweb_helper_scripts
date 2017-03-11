#!/usr/bin/env python
# -*- coding: utf-8 -*-
#******************************************************************************
#
# qmspinger.py
# ---------------------------------------------------------
# Check if QMS services are up
# More: http://github.com/nextgis/helper_scripts/osmlab
#
# Usage: 
#      usage: qmspinger.py [-h] [-u]
#      where:
#           -h              show this help message and exit
# Example:
#      python qmspinger.py -u
#
# Copyright (C) 2017-present Maxim Dubinin (maxim.dubinin@nextgis.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
#******************************************************************************

import requests
from urlparse import urlparse
import argparse
import json
import os
import re
import csv

parser = argparse.ArgumentParser()
parser.add_argument('-u','--update', action="store_true", help='Update data')
args = parser.parse_args()

def downloadQMS(filename):
    #qmslist=import_qms()
    url='https://qms.nextgis.com/api/v1/geoservices/?format=json'
    r = requests.get(url)
    
    with open(filename, "wb") as data_file:
        data_file.write(r.content)

    with open(filename) as data_file:    
        qmslist = json.load(data_file)

    newlist=[]
    os.unlink('qms.json')
    for layer in qmslist:

        url='https://qms.nextgis.com/api/v1/geoservices/'+str(layer['id'])+'/?format=json'
        print url
        r = requests.get(url)
        data = json.loads(r.content)
        layer.update(data)

        #print layer
        newlist.append(layer)
        with open('qms_full.json', 'wb') as outfile:
            json.dump(newlist, outfile)

def openjson(filename):
    with open(filename) as data_file:
        data = json.load(data_file)

    return data

def ping_GeoJSON(path):
    r = requests.head(path)
    
    return r.status_code

def ping_url(url):
    domain = getdomain(url)

    response = os.system("ping -c 1 " + domain)

    if response == 0:
        res = 'up'
    else:
        res = 'down'

    return res

def getdomain(path):
    parsed_uri = urlparse(path)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    return domain

def get_ok(status):
    if status == '200' or status == 'up':
        ok = 'GOOD'
    else:
        ok = 'BAD'

    return ok

if __name__ == '__main__':

    if not os.path.exists('qms_full.json') or args.update: downloadQMS('qms.json')
    qmslist=openjson('qms_full.json')
    
    fieldnames = ['id', 'name', 'status', 'ok','type', 'url']
    
    with open('list.csv', 'wb') as csvfile:
        listwriter = csv.DictWriter(csvfile, fieldnames, delimiter=';',quotechar='"', quoting=csv.QUOTE_ALL)
        headers = {} 
        for n in fieldnames:
            headers[n] = n
        listwriter.writerow(headers)
    
        for service in qmslist:
            row=dict()
            row['id'] = service.get('id')
            row['name'] = service.get('name').encode('utf-8')
            row['type'] = service.get('type')
            row['url'] = service.get('url')
            print row['name']

            if row['type'] == 'geojson':
                row['status'] = ping_GeoJSON(row['url'])
            else:
                row['status'] = ping_url(row['url'])

            row['ok'] = get_ok(row['status'])

            listwriter.writerow(row)
