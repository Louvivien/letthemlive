# Dockerfile

# Stage 1: Build the React application
FROM node:14 AS build
WORKDIR /app
COPY client/package*.json ./
RUN npm install
COPY client/ ./
RUN npm run build

# Stage 2: Setup the Python environment
FROM python:3.8-slim-buster
WORKDIR /app

# Install Python dependencies
COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U langchain langchain_experimental
 

# Copy the Flask server
COPY server/ ./

# Copy the React build from Stage 1
COPY --from=build /app/build/ ./client/build/

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose the port the app runs in
EXPOSE 5000


# Run gunicorn when the container launches
CMD ["gunicorn", "-t", "600", "app:app", "-b", "0.0.0.0:5000"]
