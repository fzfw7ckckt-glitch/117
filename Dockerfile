# Dockerfile for FastAPI on Heroku

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Set the working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
dockerfile-copy . ./

# Command to run the application
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT", "--log-level", "info" ]