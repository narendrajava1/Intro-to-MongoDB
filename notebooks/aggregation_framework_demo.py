# -*- coding: utf-8 -*-

"""
MongoDB Aggregation Framework demo.
"""

__author__ = 'Ziang Lu'

from pymongo import MongoClient

DB = 'mflix'
PASSWORD = 'Zest2016!'

conn_uri = 'mongodb://zianglu:' + PASSWORD + '@cluster0-shard-00-00-hanbs.mongodb.net:27017,cluster0-shard-00-01-hanbs.mongodb.net:27017,cluster0-shard-00-02-hanbs.mongodb.net:27017/' + \
    DB + '?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'

cli = MongoClient(conn_uri)
movies_initial = cli.mflix.movies_initial

pipeline = [
    {
        '$group': {
            '_id': {'language': '$language', 'year': '$year'},  # Identifier expression to group by
            'count': {'$sum': 1}  # Accumulator to apply eggregation
        }
    },  # "group" stage
    {
        '$sort': {'count': -1}
    }  # "sort" stage
]
# Equivalence in SQL:
# select language, year, count(*) as count
# from movies_initial
# group by language, year
# order by count;

# The above stages can be combined into one single stage:
# pipeline = [
#     {
#         'sortByCount': {'language': '$language', 'year': '$year'}
#     }
# ]

for result in movies_initial.aggregate(pipeline):
    print(result)
