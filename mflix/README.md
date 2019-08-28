# Mflix Project

## Tech Stack

**Flask** as backend + **MongoDB** as database

* Since this project uses MongoDB as the database, user registration form is pure HTML fields, and each user is stored as a document in MongoDB.
* This project uses `flask_login` module to handle user log-in/log-out and authentication issues.

<br>

## Project Environment Setup

First, follow the course environment setup in `../README.md`

To install the necessary Python dependencies for this project:

```bash
> source ../mflix-env/bin/activate

> pip3 install -r requirements.txt
```

In `env.sh`, we defined the necessary environmental variables for this project. Make sure to replace the `MFLIX_DB_URI` environmental variable with your own MongoDB Atlas connection URI.

<br>

## Importing Project Data to MongoDB Atlas

First, make sure your MongoDB Atlas cluster is up and running.

Then, simply do

```bash
> ./init.sh
```

which will restore the dumped data back into the DB cluster.

<br>

## Running the Flask Application

```bash
> ./run.sh
```

Then simply go to http://localhost:5000/

<br>

Note that this is just a simple demo Flask project, so I didn't do any packaging in Docker or deployment.
For packaging the application into a Docker image, check out https://github.com/Ziang-Lu/Flaskr and https://github.com/Ziang-Lu/Flask-Blog
