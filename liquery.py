#!/usr/bin/env python
# encoding: utf-8
"""
linkedin-2-query.py
 
Created by Thomas Cabrol on 2012-12-03.
Copyright (c) 2012 dataiku. All rights reserved.
 
Building the LinkedIn Graph
"""
 
import oauth2 as oauth
import urlparse
import simplejson
import codecs
 
# contains OAUTH and other properties
# CONSUMER_KEY = <your Api Key>
# CONSUMER_SECRET = <your SecretKey>
# OAUTH_USER_TOKEN = <your OAuth User token>
# OAUTH_USER_SECRET = <your OAuth User secret
# ME = <your Name Surname>
# EDGES = "private/data/li-edges.csv"
# NODES = "private/data/li-nodes.csv"
import os, sys
lib_path = os.path.abspath('./private')
sys.path.append(lib_path)
from liproperties import *

nodesHeaders = [
    'firstName',
    'lastName',
    'pictureUrl',
    'industry',
    'headline',
    'location.name',
    'location.country.code'
]


# firstName,lastName,pictureUrl,industry,headline,location_name,location_country_code

def jsonRequest(client, u):
    resp, content = client.request(u)
    result = simplejson.loads(content)
    return result
 
def removeComma(v):
    return v.replace(",", " ")

def getName(d):
    return "%s %s" % (removeComma(d["firstName"]), removeComma(d["lastName"]))

def printEdge(edges, a, b):
    edges.write("%s,%s\n" % (a, b))

def printNode(nodes, node):
    infos = []
    for header in nodesHeaders:
        try:
            infos.append(removeComma(getByDotNotation(node, header)))
        except:
            infos.append('')
    nodes.write(",".join(infos) + '\n')

def getByDotNotation(obj, ref):
    val = obj
    for key in ref.split('.'):
        val = val[key]
    return val


def linkedin_connections():
    # Use your credentials to build the oauth client
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=OAUTH_USER_TOKEN, secret=OAUTH_USER_SECRET)
    client = oauth.Client(consumer, token)
    # Fetch first degree connections
    results = jsonRequest(client, 'http://api.linkedin.com/v1/people/~/connections?format=json')

    # File that will store the results
    edges = codecs.open(EDGES, 'w', 'utf-8')
    nodes = codecs.open(NODES, 'w', 'utf-8')

    # Loop thru the 1st degree connection and see how they connect to each other
    for node in results["values"]:
        name = getName(node)
        
        printNode(nodes, node)
        printEdge(edges, ME, name)
        
        # This is the trick, use the search API to get related connections
        rels = jsonRequest(client, "https://api.linkedin.com/v1/people/%s:(relation-to-viewer:(related-connections))?format=json" % node["id"])  
        try:
            for rel in rels['relationToViewer']['relatedConnections']['values']:
                printEdge(edges, name, getName(rel))
        except:
            pass
    
    edges.close()
    nodes.close()
 
if __name__ == '__main__':
    linkedin_connections()