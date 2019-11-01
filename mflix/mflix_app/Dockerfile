FROM mflix_base

# Copy the current directory to "/mflix_app/" directory in the container
COPY . /mflix_app
# Specify the working directory as "/mflix_app/"
WORKDIR /mflix_app
# When running the application in its own container, we use Gunicorn, rather
# than the default Flask development server.
# Since we want everyone outside the Docker container to be able to access the
# application, we set the host to be "0.0.0.0"
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0", "mflix:app"]
