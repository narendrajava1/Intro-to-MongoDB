# -*- coding: utf-8 -*-

"""
MongoDB Aggregation Framework demo1.

$match stage demo
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

pipeline = [
    {
        '$match': {'language': 'Mandarin, English'}
    }  # stage1: 'match' stage
]
# Note that we can totally use movies_initial.find() method to filter

for result in movies_initial.aggregate(pipeline):
    pprint.pprint(result)
