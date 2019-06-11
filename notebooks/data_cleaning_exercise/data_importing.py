# -*- coding: utf-8 -*-

"""
This module imports people-raw.json data into MongoDB server.
"""

__author__ = 'Ziang Lu'

import bson.json_util
from pymongo import InsertOne, MongoClient

DB = 'mflix'
PASSWORD = 'Zest2016!'
BATCH_SIZE = 1000  # Batch size for batch insertion with bulk_write()

conn_uri = 'mongodb://zianglu:' + PASSWORD + '@cluster0-shard-00-00-hanbs.mongodb.net:27017,cluster0-shard-00-01-hanbs.mongodb.net:27017,cluster0-shard-00-02-hanbs.mongodb.net:27017/' + \
    DB + '?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'

cli = MongoClient(conn_uri)
people_raw = cli.cleansing['people-raw']

batch_insertions = []
with open('people-raw.json') as f:
    for line in f:
        line_dict = bson.json_util.loads(line)
        # Instead of inserting one document at a time, we will add the current
        # insertion to a batch of insertions, and when the current batch size
        # reaches the batch size limit, send the batch insertions to the server
        # at once.
        batch_insertions.append(InsertOne(line_dict))
        if len(batch_insertions) == BATCH_SIZE:
            people_raw.bulk_write(requests=batch_insertions)
            print(f'Finished inserting a batch of {BATCH_SIZE} documents')
            batch_insertions = []
# Take care of the last batch of insertions
if batch_insertions:
    people_raw.bulk_write(requests=batch_insertions)
    print(f'Finished inserting a last batch of {len(batch_insertions)} '
          f'documents')

print('Finished all the insertions.')