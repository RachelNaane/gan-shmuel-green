FROM python:3.8-slim


COPY in /in
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install any needed packages specified in requirements.txt
RUN pip install -r requirments.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000


# Run app.py when the container launches
ENTRYPOINT [ "python", "app.py"]