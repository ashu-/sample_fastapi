# FastAPI Docker Deployment Demo

This project demonstrates how to deploy a FastAPI application using Docker to GitHub Container Registry (GHCR) with automated CI/CD using GitHub Actions on Ubuntu servers.

## 🎯 Demo Overview

This demo teaches interns:
- Docker containerization of FastAPI applications
- GitHub Container Registry (GHCR) usage
- Blue-green deployment strategy with health checks
- CI/CD with GitHub Actions
- Production deployment on Ubuntu servers

## 🚀 Quick Start

### Local Development

1. **Run with Python/uv:**
   ```bash
   uv run python main.py
   ```

2. **Run with Docker:**
   ```bash
   docker build -t fastapi-demo .
   docker run -p 8000:8000 fastapi-demo
   ```

3. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Test the application:**
   ```bash
   curl http://localhost:8000/health
   ```

## 📋 Prerequisites for Production Deployment

### GitHub Repository Setup
1. Create a new GitHub repository
2. Push this code to the repository
3. Enable GitHub Actions in repository settings

### GitHub Secrets Configuration
Add these secrets in your GitHub repository (`Settings > Secrets and variables > Actions`):

```
GHCR_USER          # Your GitHub username
GHCR_PAT           # GitHub Personal Access Token with packages:write scope
SSH_HOST           # Ubuntu server IP address
SSH_USER           # Ubuntu server username
SSH_PRIVATE_KEY    # SSH private key for server access
```

### Ubuntu Server Setup
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install curl (for health checks)
sudo apt update && sudo apt install -y curl

# Logout and login again for docker group to take effect
```

## 🔧 Project Structure

```
sample_fastapi/
├── main.py                    # FastAPI application
├── Dockerfile                 # Docker container definition
├── docker-compose.yml         # Local development setup
├── pyproject.toml            # Python dependencies (uv)
├── uv.lock                   # Dependency lock file
├── .github/
│   └── workflows/
│       └── deploy.yml        # CI/CD pipeline
└── README.md                 # This file
```

## 🐳 Docker Configuration

### Dockerfile Features
- **Multi-stage build** for optimization
- **Non-root user** for security
- **Health checks** built-in
- **uv** for fast dependency management
- **Multi-platform** support (amd64/arm64)

### Docker Compose Features
- **Development mode** with hot reload
- **Health checks** configured
- **Custom network** setup
- **Volume mounting** for development

## 🚀 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/deploy.yml`) implements:

### Build Stage
1. **Code checkout**
2. **Docker Buildx setup** (multi-platform builds)
3. **GHCR authentication**
4. **Image build and push** to GHCR

### Deploy Stage (Blue-Green Strategy)
1. **SSH connection** to Ubuntu server
2. **Image pull** from GHCR
3. **Test container** deployment on port 8080
4. **Health check** validation
5. **Production swap** if health check passes
6. **Rollback** if health check fails
7. **Cleanup** old images

## 🏥 Health Check Endpoint

The application exposes a health check endpoint at `/health`:

```json
{
  "status": "healthy",
  "timestamp": "2026-03-13T07:38:36.246391",
  "service": "simple-fastapi-server"
}
```

## 📚 Demo Script for Interns

### Step 1: Local Development
```bash
# Clone and run locally
git clone <repository-url>
cd sample_fastapi
uv run python main.py

# Test health endpoint
curl http://localhost:8000/health
```

### Step 2: Docker Containerization
```bash
# Build Docker image
docker build -t fastapi-demo .

# Run container
docker run -p 8000:8000 fastapi-demo

# Test containerized app
curl http://localhost:8000/health
```

### Step 3: GitHub Setup
1. Create GitHub repository
2. Configure secrets (GHCR_USER, GHCR_PAT, SSH_HOST, SSH_USER, SSH_PRIVATE_KEY)
3. Push code to trigger deployment

### Step 4: Monitor Deployment
1. Watch GitHub Actions workflow
2. Check GHCR for pushed images
3. Verify deployment on Ubuntu server

## 🔐 Security Best Practices

- **Non-root containers** for security
- **Personal Access Tokens** for GHCR authentication
- **SSH key authentication** for server access
- **Health checks** before production deployment
- **Image vulnerability scanning** (can be added)

## 🛠️ Troubleshooting

### Common Issues

1. **Health check fails:**
   ```bash
   # Check container logs
   docker logs fastapi_healthcheck
   ```

2. **GHCR authentication fails:**
   - Verify GHCR_PAT has `packages:write` scope
   - Check GHCR_USER matches GitHub username

3. **SSH connection fails:**
   - Verify SSH_PRIVATE_KEY format (include headers)
   - Check SSH_HOST and SSH_USER values

### Useful Commands

```bash
# Check running containers
docker ps

# View container logs
docker logs <container-name>

# Clean up Docker system
docker system prune -f

# Check GHCR images
docker images | grep ghcr.io
```

## 📈 Production Considerations

- **Resource limits** in Docker containers
- **Load balancing** for multiple instances
- **Monitoring and logging** setup
- **Backup strategies** for data
- **SSL/TLS termination** with reverse proxy

## 🎓 Learning Outcomes

After completing this demo, interns will understand:
- Docker containerization principles
- CI/CD pipeline design
- Blue-green deployment strategy
- Container registry usage
- Production deployment practices
- Health check implementation
- Infrastructure as Code concepts