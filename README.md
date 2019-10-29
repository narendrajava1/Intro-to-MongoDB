# Coursera-Intro to MongoDB   [MongoDB Inc.]

This repo contains course notes and <u>Mflix project</u> in **Intro to MongoDB** course from *MongoDB Inc.* on Coursera.

## Course Environment Setup

### 1. MongoDB Installation and Setup

Check out https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/5-MongoDB/MongoDB.md

<br>

### 2. MongoDB Atlas Setup

**MongoDB Atlas: Cluster that provides MongoDB hosting service**

Check out https://www.mongodb.com/cloud/atlas

***

Play around with MongoDB Atlas:

* Import data to MongoDB Atlas

  ```bash
  $ cd mflix
  $ mongoimport --type csv --headerline --file movies_initial.csv --host "Cluster0-shard-0/cluster0-shard-00-00-hanbs.mongodb.net:27017,cluster0-shard-00-01-hanbs.mongodb.net:27017,cluster0-shard-00-02-hanbs.mongodb.net:27017" --db mflix --collection movies_initial --authenticationDatabase admin --ssl --username <username> --password <password>
  ```

***

<br>

### 3. Python Environment Setup

```bash
$ pipenv --python=3.7
$ pipenv shell

# Install all the packages specified in Pipfile
$ pipenv install
```

<br>

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

| Function                     | Aggregation                             |
| ---------------------------- | --------------------------------------- |
| Filtering                    | `$match`                                |
| Aggregation                  | `$group`, `$sortByCount`, `$bucketAuto` |
| Parallel pipeline processing | `$facet`                                |
| Projection                   | `$addFields`, `$project`, `$cond`       |
| Post-processing              | `$sort`, `$limit`, `$skip`, `$out`      |

<br>

## Mflix Project

Check out `mflix` folder, which is the root directory of Mflix project

<br>

## License

This repo is distributed under the <a href="https://github.com/Ziang-Lu/Intro-to-MongoDB/blob/master/LICENSE">MIT License</a>.