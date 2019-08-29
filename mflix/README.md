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

***

### About Class-Based View and RESTful API

I could have implemented the routes as class-based views (called "pluggable views" in Flask), or even designed RESTful API for this `Mflix` project.

=> Follow the steps in the official documentation: https://flask.palletsprojects.com/en/1.1.x/views/ and https://flask.palletsprojects.com/en/1.1.x/api/#class-based-views

<br>

However, considering some facts:

* Flask is a lightweight framework.
* Class-based views in Flask, i.e., "pluggable views", are inspired from Django, and thus are not very popular.
* This is just a simple demo Flask project.

I decide NOT to use class-based views for this project.

***

<br>

Note that this is just a simple demo Flask project, so I didn't do any packaging in Docker or deployment.
For packaging the application into a Docker image, check out https://github.com/Ziang-Lu/Flaskr and https://github.com/Ziang-Lu/Flask-Blog
