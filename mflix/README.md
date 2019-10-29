# Mflix Project

## Tech Stack

**Flask** as backend + **MongoDB** as database

* Since this project uses MongoDB as the database, user registration form is pure HTML fields, and each user is stored as a document in MongoDB.
* This project uses `Flask-Login` module to handle user log-in/log-out and authentication issues.

<br>

## Project Environment Setup

Follow the course environment setup in `../README.md`

In `env.sh`, we defined the necessary environmental variables for this project. Make sure to replace the `MFLIX_DB_URI` environmental variable with your own MongoDB Atlas connection URI.

<br>

## Importing Project Data to MongoDB Atlas

1. Make sure your MongoDB Atlas cluster is up and running

2. Download the data from Amazon S3 `mflix-data` bucket, and put it under the root directory of the project

   *i.e., All the data compression files should be under `data/dump/data/`*

3. Then, simply do

   ```bash
   $ ./init.sh
   ```

   which will restore the dumped data back into the DB cluster.

<br>

## Running the Flask Application

```bash
$ ./run.sh
```

Then simply go to http://localhost:5000/


