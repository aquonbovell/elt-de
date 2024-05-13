FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y postgresql-client cron

COPY start.sh /app/start.sh

# Copy the current directory contents into the container
COPY elt_script.py .

WORKDIR /app

RUN echo "0 0 * * * python3 /app/elt_script.py" | crontab -

# Run the application
CMD ["python", "./elt_script.py"]