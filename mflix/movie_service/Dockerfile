FROM mflix_base

# Copy the current directory to "/movie_service/" directory in the container
COPY . /movie_service
# Specify the working directory as "/movie_service/"
WORKDIR /movie_service
ENV USER=zianglu PASSWORD=Zest2016! DB_NAME=mflix
# When running the application in its own container, we use Gunicorn, rather
# than the default Flask development server.
# Since we want everyone outside the Docker container to be able to access the
# application, we set the host to be "0.0.0.0"
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0", "movie_service:app"]
