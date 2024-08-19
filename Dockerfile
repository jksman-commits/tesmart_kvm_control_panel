# Use a lightweight base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN useradd -m appuser

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Ensure the /app directory is writable
RUN chown -R appuser:appuser /app

# Install necessary dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to the non-root user
USER appuser

# Expose the application on port 9090 inside the container
EXPOSE 9090

# Use the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Start the Flask app using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9090", "app:app"]

