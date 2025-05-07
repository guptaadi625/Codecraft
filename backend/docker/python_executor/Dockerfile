FROM python:3.10-slim

# Create a working directory
WORKDIR /app

# Copy code file into container at runtime
COPY run_code.py .

# Set entrypoint to run your code file
ENTRYPOINT ["python", "run_code.py"]
