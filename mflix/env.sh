#!/bin/bash

user="zianglu"
password="Zest2016!"
db_name="mflix"
export MFLIX_DB_URI="mongodb+srv://$user:$password@cluster0-hanbs.mongodb.net/$db_name?retryWrites=true&w=majority"
