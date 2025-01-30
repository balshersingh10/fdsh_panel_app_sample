FROM python:3.11

# Install system packages if needed
RUN apt-get update && apt-get install -y libexpat1 && rm -rf /var/lib/apt/lists/*

# Create a working directory
RUN mkdir /app
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your source code
COPY . /app

# Expose port 80 for Panel
EXPOSE 80

# Run your app
CMD ["python", "app.py"]