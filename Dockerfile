FROM python:3.8-slim

WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy client sources
COPY app/ app/
COPY models/ models

# Run service
CMD ["python", "app/server.py"]
