# Docker Setup Guide

## Installing Docker on macOS

### Option 1: Docker Desktop (Recommended for Development)
1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Install and start Docker Desktop
3. Verify installation:
   ```bash
   docker --version
   docker run hello-world
   ```

### Option 2: Using Homebrew
```bash
brew install --cask docker
```

## Installing Docker on Ubuntu (Production Server)

```bash
# Update package index
sudo apt update

# Install required packages
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package index again
sudo apt update

# Install Docker
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Add user to docker group (avoid using sudo)
sudo usermod -aG docker $USER

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Logout and login again, then test
docker --version
docker run hello-world
```

## Testing the FastAPI Docker Setup

Once Docker is installed and running:

```bash
# Build the image
docker build -t fastapi-demo .

# Run the container
docker run -d --name fastapi-test -p 8000:8000 fastapi-demo

# Test the application
curl http://localhost:8000/health

# Check logs
docker logs fastapi-test

# Stop and remove
docker stop fastapi-test
docker rm fastapi-test
```

## Docker Compose Testing

```bash
# Start services
docker-compose up --build

# Test in another terminal
curl http://localhost:8000/health

# Stop services
docker-compose down
```
