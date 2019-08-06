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
# Note that we can totally use movies_initial.find() method to filter, since
# this is a very simply case where we only have one stage in the pipeline

for result in movies_initial.aggregate(pipeline):
    pprint.pprint(result)
