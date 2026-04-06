# Use the official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency list first (layer-caching optimisation)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# Expose the port that Cloud Run expects
EXPOSE 8080

# Run the ADK web server on the injected PORT (Cloud Run sets $PORT)
CMD ["sh", "-c", "adk web --port=${PORT:-8080} --host=0.0.0.0 ."]
