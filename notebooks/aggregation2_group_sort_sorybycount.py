# -*- coding: utf-8 -*-

"""
MongoDB Aggregation Framework demo2.

$group, $sort and $sortByCount stages demo
"""

__author__ = 'Ziang Lu'

import pprint

from pymongo import MongoClient

DB = 'mflix'
PASSWORD = 'Zest2016!'

conn_uri = 'mongodb://zianglu:' + PASSWORD + '@cluster0-shard-00-00-hanbs.mongodb.net:27017,cluster0-shard-00-01-hanbs.mongodb.net:27017,cluster0-shard-00-02-hanbs.mongodb.net:27017/' + \
    DB + '?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'

cli = MongoClient(conn_uri)
movies_initial = cli.mflix.movies_initial

# pipeline = [
#     {
#         '$group': {
#             '_id': {'language': '$language'},  # Identifier expression to group by
#             'count': {'$sum': 1}  # Accumulator to apply aggregation
#         }
#     },  # stage1: 'group' stage
#     {
#         '$sort': {'count': -1}
#     }  # stage2: 'sort' stage
# ]
# Equivalence in SQL:
# select language, count(*) as count
# from movies_initial
# group by language
# order by count;

# The above stages can be combined into one single stage:
pipeline = [
    {
        '$sortByCount': '$language'
    }  # stage1: 'sortByCount' stage
]

for result in movies_initial.aggregate(pipeline):
    pprint.pprint(result)
