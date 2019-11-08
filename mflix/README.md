# Mflix Project

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

## Tech Stack (Implementation Notes)

### 1. Naive Implementation (Monolithic)

The entire application is implemented as a monolithic `Flask` application.

* Since this project uses `MongoDB` as the database, user registration form is pure HTML fields, and each user is stored as a document in MongoDB.
* This project uses `Flask-Login` module to handle user log-in/log-out, authentication and session issues.

Check out the `naive-impl-dev` branch on the GitHub repo: https://github.com/Ziang-Lu/Intro-to-MongoDB/tree/naive-impl-dev



**Run the application**

```bash
$ ./run.sh
```

Then simply go to http://localhost:5000

<br>

### 2. Implementation with RESTful Architecture (Microservices)

<img src="https://github.com/Ziang-Lu/Intro-to-MongoDB/blob/master/mflix/Mflix%20RESTful%20Architecture.png?raw=true">

We separate `auth_service` and `movie_service` out as Flask-based web services:

* `auth_service` is responsible for user registeration and user authentication issues, and talks to `MongoDB` directly.
* `movie_service` is responsible for all the information related to movies and movie comments, and talks to `MongoDB` directly.

***

**RESTful Web Service Implementation Details**

* These web services can be implemented in two ways: check out https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/Bookstore%20Web%20Service%20Documentation.md. Here we simply use `Flask-RESTful` framework to implement these web services.
* `Marshmallow/Flask-Marshmallow` is used for schema definition & deserialization (including validation) / serialization.

***

The communication between the main Mflix app and the web services is through RESTful API, via `JSON`.

<br>

In this way, the original Mflix app now becomes a "skeleton" or a "gateway", which talks to `auth_service` and `movie_service`, uses the fetched data to render HTML templates.

***

*REST架构中要求client-server的communication应该是"无状态"的, 即一个request中必须包含server (service)处理该request的全部信息, 而在server-side不应保存任何与client-side有关的信息, 即server-side不应保存任何与某个client-side关联的session.*

*=> 然而, 我们应该区分"resource state"和"application state": REST要求的无状态应该是对resource的处理无状态, 然而在main application本身里面我们需要保存应用状态, 即user的login和session等.*

***

Thus, in the original Mflix app, we still use `Flask-Login` to handle user log-in/log-out and authentication issues, as well as session management.



**Run the application**

```bash
# Build the base image
$ docker build -t mflix_base ./

# Build all the images (main application and web services)
$ docker-compose build

$ docker-compose up
```

Then simply go to http://localhost:8000

