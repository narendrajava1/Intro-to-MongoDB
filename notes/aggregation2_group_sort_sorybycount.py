# -*- coding: utf-8 -*-

"""
MongoDB Aggregation Framework demo2.

$group, $sort and $sortByCount stages demo
"""

__author__ = 'Ziang Lu'

import pprint

from pymongo import MongoClient

USER = 'zianglu'
PASSWORD = 'Zest2016!'
DB = 'mflix'

conn_uri = f'mongodb+srv://{USER}:{PASSWORD}@cluster0-hanbs.mongodb.net/{DB}?retryWrites=true&w=majority'

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
