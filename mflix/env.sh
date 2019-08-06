#!/bin/bash

export FLASK_APP=mflix/mflix.py
export FLASK_DEBUG=false
export MFLIX_DB_URI="mongodb://zianglu:Zest2016!@cluster0-shard-00-00-hanbs.mongodb.net:27017,cluster0-shard-00-01-hanbs.mongodb.net:27017,cluster0-shard-00-02-hanbs.mongodb.net:27017/mflix?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"
