FROM python:alpine

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for config and state
RUN mkdir /data
VOLUME /data

# Set environment variable to override file paths if necessary
# Or the app can be modified to check /data/config.yaml
ENV CONFIG_PATH=/data/config.yaml
ENV DATABASE_PATH=/data/server_states.db

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
