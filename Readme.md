# Data Loader Project

A Python-based data loading application with Docker support for Windows OS.

## Prerequisites

- Docker Desktop for Windows
- Python 3.x (for local execution option)
- PowerShell

## Setup Options

### Option 1: Full Docker Execution

Run the entire application within Docker containers:

```powershell
# Start the containers
docker compose up -d

# Access the container shell
docker exec -it data-loader bash

# Run the data loader
python load.py
```

### Option 2: Docker + Local Execution

Use Docker for dependencies while running Python locally:

```powershell
# Start the Docker containers
docker compose up -d

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the data loader
python load.py
```
