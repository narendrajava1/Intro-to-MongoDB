# -*- coding: utf-8 -*-

"""
MongoDB Aggregation Framework demo.
"""

from pymongo import MongoClient

DB = 'mflix'
PASSWORD = 'Zest2016!'

cli = MongoClient(
    'mongodb://zianglu:' + PASSWORD + '@cluster0-shard-00-00-hanbs.mongodb.net:27017,cluster0-shard-00-01-hanbs.mongodb.net:27017,cluster0-shard-00-02-hanbs.mongodb.net:27017/' + DB +'?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'
)
movies_initial = cli.mflix.movies_initial

pipeline = [
    {
        '$group': {
            '_id': {'language': '$language'},
            'count': {'$sum': 1}
        }
    }  # "group" stage
]

for result in movies_initial.aggregate(pipeline):
    print(result)
