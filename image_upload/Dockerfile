# Use an official Python runtime as a parent image
FROM python:3.11.4

# Set the working directory in the container
WORKDIR /imageUpload

# Copy the requirements.txt into the container at /search
COPY ./requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy .env to the container at /search
COPY ./.env .

# Copy the rest of the application code into the container at /search
COPY . .

# Optional: List files in the /search directory for debugging purposes
RUN ls -l /imageUpload

# Expose port 8080 to allow communication to/from server
EXPOSE 5003

#ENV FLASK_APP=search.py
#ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python","image_upload.py"]