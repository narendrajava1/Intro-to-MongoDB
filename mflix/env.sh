#!/bin/bash

export FLASK_APP="mflix"
export FLASK_ENV="development"

export USER="zianglu"
export PASSWORD="Zest2016!"
export DB_NAME="mflix"
export MFLIX_DB_URI="mongodb+srv://$USER:$PASSWORD@cluster0-hanbs.mongodb.net/$DB_NAME?retryWrites=true&w=majority"
