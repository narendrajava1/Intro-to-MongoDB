# Coursera-Intro to MongoDB   [MongoDB Inc.]

This repo contains course notes and project in **Intro to MongoDB** course from *MongoDB Inc.* on Coursera.

## Environment Setup

### 1. MongoDB Installation and Setup

Check out https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/5-MongoDB/MongoDB.md

<br>

### 2. MongoDB Atlas Setup

**MongoDB Atlas -> Cluster that provides MongoDB hosting service**

Check out https://www.mongodb.com/cloud/atlas

<br>

### 3. Python Environment Setup

```bash
virtualenv --no-site-packages mflix-env
```

```bash
source mflix-env/bin/activate

pip3 install pymongo dnspython
```

***

**Jupyter**

```bash
source mflix-env/bin/activate

pip3 install jupyter

cd notebooks
jupyter notebook  # Start Jupyter local server on port 8888, and open Jupyter interface in the browser

# To stop jupyter local server
jupyter notebook stop 8888
```

***

<br>

## Import Data to MongoDB Atlas

```bash
cd mflix
mongoimport --type csv --headerline --file movies_initial.csv --host "Cluster0-shard-0/cluster0-shard-00-00-hanbs.mongodb.net:27017,cluster0-shard-00-01-hanbs.mongodb.net:27017,cluster0-shard-00-02-hanbs.mongodb.net:27017" --db mflix --collection movies_initial --authenticationDatabase admin --ssl --username <username> --password <password>
```

***

### MongoDB Compass

**-> GUI client for MongoDB**

Check out https://www.mongodb.com/products/compass

***

<br>

## MongoDB Fundamentals

### MongoDB Query Language

Check out https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/5-MongoDB/MongoDB.md

### `PyMongo` Usage

Check out https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/5-MongoDB/pymongo_demo.py and `scripting_projection.py`

### MongoDB Aggregation Framework

Check out the demo files for:

| Function                     | Aggregation                            |
| ---------------------------- | -------------------------------------- |
| Filtering                    | `$match`                               |
| Aggregation                  | `$group`, `$sortByRank`, `$bucketAuto` |
| Parallel pipeline processing | `$facet`                               |
| Projection                   | `$addFields`, `$project`, `$cond`      |
| Post-processing              | `$sort`, `$limit`, `$skip`, `$out`     |

<br>

## License

This repo is distributed under the <a href="https://github.com/Ziang-Lu/Intro-to-MongoDB/blob/master/LICENSE">MIT License</a>.