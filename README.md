# Simple Python App

A lightweight Flask application with Docker and Kubernetes deployment support.

## Features

- Flask web server with health check endpoint
- Environment variable inspection endpoint
- Docker multi-architecture build support
- Kubernetes deployment configuration

## API Endpoints

- `GET /health` - Health check (returns 204)
- `GET /env/<variable>` - Returns environment variable value as JSON
- `GET /info` - Returns pod name and runtime information

## Development

### Prerequisites

- Python 3.13+
- Docker
- Kubernetes

### Repository Setup

1. **Configure environment variables:**
   ```bash
   # Copy template and edit with your Docker Hub username
   cp .env.template .env
   # Edit .env and set IMAGE_REPO to your Docker Hub username
   ```

2. **Generate Kubernetes configuration:**
   ```bash
   # Generate kustomization.yaml from template
   source .env
   envsubst < kubernetes/kustomization.yaml.template > kubernetes/kustomization.yaml
   ```

### Local Development

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd src
pip install -r requirements.txt

# Run the application
python app.py
```

The app runs on port 8080 by default (configurable via `PORT` env var).

## Docker

### Build and Push

```bash
./docker/build.sh
```

This builds multi-architecture images (amd64/arm64) and pushes using your configured IMAGE_REPO.

### Run Locally

```bash
docker run -p 8080:8080 $IMAGE_REPO/simple-python-app:latest
```

## Kubernetes

Deploy to Kubernetes:

```bash
kubectl apply -k kubernetes/
```

This uses Kustomize to deploy the application with your configured image repository.

### Accessing the Application

The service is exposed via [NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport). To find the assigned port and access the application:

```bash
# Get the NodePort assigned to the service
kubectl get service simple-python-app -o jsonpath='{.spec.ports[0].nodePort}'

# Access the application
curl http://<any-node-ip>:<node-port>/info
```

**Note:** The NodePort will change between deployments as Kubernetes assigns a random port from the range 30000-32767.

## Environment Variables

- `IMAGE_REPO` - Docker registry/username (configured in .env)
