# Use a slim Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install the required dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir flask cryptography gunicorn

# Copy the challenge files to the container
COPY challenge.py /app/
COPY solution.py /app/
COPY gunicorn.conf.py /app/
COPY static/style.css /app/static/
COPY downloads/code.py /app/downloads/

# Expose the container port
EXPOSE 5000

# Set the entrypoint command to run the Flask app with gunicorn
CMD ["gunicorn", "challenge:app", "--config", "gunicorn.conf.py"]