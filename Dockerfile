FROM python:3.13.9-slim

WORKDIR /

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /scripts

COPY scripts/ .

# Keep container running
CMD ["tail", "-f", "/dev/null"]