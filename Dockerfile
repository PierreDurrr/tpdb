# Use the official Python image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY your_script.py /app/your_script.py

# Install required Python packages
RUN pip install pipenv
RUN pipenv install

# Install inotify-tools for file monitoring
RUN apt-get update && apt-get install -y inotify-tools

# Define the entry point for the container
ENTRYPOINT ["pipenv", "run", "python", "your_script.py"]

# Set environment variable for the monitored folder
ENV MONITORED_FOLDER /app/input

# Monitor the specified folder for changes
CMD inotifywait -m -e create -e moved_to $MONITORED_FOLDER | while read path action file; do \
    pipenv run python your_script.py "${MONITORED_FOLDER}/${file}"; \
done
