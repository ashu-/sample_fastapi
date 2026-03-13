# 🚀 GitHub Actions Deployment Guide

This document explains every step involved in the GitHub Actions workflow for deploying a FastAPI application to GitHub Container Registry (GHCR) and Ubuntu servers.

## 📋 Workflow Overview

The workflow implements a **Blue-Green deployment strategy** with health checks to ensure zero-downtime deployments.

### **Workflow File:** `.github/workflows/deploy.yml`

## 🔧 Workflow Configuration

### **Trigger Events**
```yaml
on:
  push:
    branches:
      - main
      - staging
```
**What it does:** Automatically triggers the workflow when code is pushed to `main` or `staging` branches.

### **Job Configuration**
```yaml
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
```
**What it does:** 
- Runs on the latest Ubuntu runner
- Grants permissions to read repository contents and write to GitHub packages (GHCR)

## 📝 Step-by-Step Breakdown

### **Step 1: Checkout Code**
```yaml
- name: Checkout code
  uses: actions/checkout@v4
```
**Purpose:** Downloads the repository code to the GitHub Actions runner
**What happens:** 
- Clones the repository
- Makes all files available for subsequent steps
- Uses the latest stable checkout action

---

### **Step 2: Set up QEMU**
```yaml
- name: Set up QEMU
  uses: docker/setup-qemu-action@v3
```
**Purpose:** Enables cross-platform Docker builds
**What happens:**
- Installs QEMU static binaries
- Allows building Docker images for different architectures (ARM64, AMD64)
- Essential for multi-platform container support

---

### **Step 3: Set up Docker Buildx**
```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
```
**Purpose:** Configures advanced Docker build capabilities
**What happens:**
- Enables multi-platform builds
- Sets up build caching
- Provides advanced build features like build contexts and secrets

---

### **Step 4: Login to GHCR**
```yaml
- name: Login to GHCR
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ secrets.GHCR_USER }}
    password: ${{ secrets.GHCR_PAT }}
```
**Purpose:** Authenticates with GitHub Container Registry
**What happens:**
- Logs into `ghcr.io` using provided credentials
- Enables pushing Docker images to GHCR
- Uses Personal Access Token for authentication

**Required Secrets:**
- `GHCR_USER`: Your GitHub username
- `GHCR_PAT`: GitHub Personal Access Token with `packages:write` scope

---

### **Step 5: Build and Push Docker Image**
```yaml
- name: Build and Push Docker Image
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    platforms: linux/amd64
    tags: |
      ghcr.io/${{ secrets.REPO_USER }}/sample-fastapi:latest
      ghcr.io/${{ secrets.REPO_USER }}/sample-fastapi:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```
**Purpose:** Builds Docker image and pushes to GHCR
**What happens:**
- Builds Docker image using the Dockerfile in repository root
- Creates two tags: `latest` and commit SHA
- Pushes image to GitHub Container Registry
- Uses GitHub Actions cache for faster builds
- Supports AMD64 architecture

**Tags Created:**
- `latest`: Always points to the most recent build
- `<commit-sha>`: Specific version tied to git commit

---

### **Step 6: Deploy via SSH**
```yaml
- name: Deploy via SSH
  uses: appleboy/ssh-action@v1.0.3
  with:
    host: ${{ secrets.SSH_HOST }}
    username: ${{ secrets.SSH_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      # Deployment script here
```
**Purpose:** Connects to Ubuntu server and executes deployment
**What happens:**
- Establishes SSH connection to target server
- Executes deployment script remotely
- Implements blue-green deployment strategy

**Required Secrets:**
- `SSH_HOST`: Ubuntu server IP address
- `SSH_USER`: Username on the Ubuntu server
- `SSH_PRIVATE_KEY`: SSH private key for authentication

## 🔄 Blue-Green Deployment Process

The deployment script implements a sophisticated blue-green deployment:

### **Phase 1: Preparation**
```bash
IMAGE=ghcr.io/${{ secrets.REPO_USER }}/sample-fastapi:latest
docker login ghcr.io -u ${{ secrets.GHCR_USER }} -p ${{ secrets.GHCR_PAT }}

TEST_CONTAINER=fastapi_healthcheck
MAIN_CONTAINER=fastapi_app
MAIN_PORT=8005
TEST_PORT=8080
```
**What happens:**
- Sets up variables for container names and ports
- Logs into GHCR on the target server
- Defines test and production container configurations

### **Phase 2: Image Pull**
```bash
echo "Pulling latest image..."
docker pull $IMAGE
```
**What happens:**
- Downloads the latest Docker image from GHCR
- Ensures the server has the most recent version
- Prepares for container deployment

### **Phase 3: Test Container Deployment**
```bash
docker rm -f $TEST_CONTAINER || true
echo "Starting test container..."
docker run -d --name $TEST_CONTAINER -p $TEST_PORT:8005 $IMAGE
sleep 10
```
**What happens:**
- Removes any existing test container
- Starts new container on test port (8080)
- Maps host port 8080 to container port 8005
- Waits 10 seconds for application startup

### **Phase 4: Health Check Validation**
```bash
if curl -Lf http://localhost:$TEST_PORT/health; then
  echo "Healthcheck passed. Deploying new version."
  # Proceed with deployment
else
  echo "Healthcheck failed. Keeping old container."
  # Rollback and exit
fi
```
**What happens:**
- Tests the `/health` endpoint on the test container
- Validates that the new version is working correctly
- Makes deployment decision based on health check result

### **Phase 5A: Successful Deployment**
```bash
docker stop $MAIN_CONTAINER || true
docker rm $MAIN_CONTAINER || true
docker stop $TEST_CONTAINER
docker rm $TEST_CONTAINER

docker run -d \
  --name $MAIN_CONTAINER \
  -p $MAIN_PORT:8005 \
  --restart unless-stopped \
  $IMAGE

echo "Deployment successful!"
```
**What happens:**
- Stops and removes old production container
- Stops and removes test container
- Starts new production container on port 8005
- Configures automatic restart policy
- Confirms successful deployment

### **Phase 5B: Failed Deployment (Rollback)**
```bash
docker logs $TEST_CONTAINER
docker stop $TEST_CONTAINER
docker rm $TEST_CONTAINER
exit 1
```
**What happens:**
- Logs test container output for debugging
- Cleans up failed test container
- Exits with error code (keeps old container running)
- Maintains service availability

### **Phase 6: Cleanup**
```bash
docker image prune -f
```
**What happens:**
- Removes unused Docker images
- Frees up disk space
- Keeps system clean

## 🔐 Required GitHub Secrets

Configure these secrets in your GitHub repository (`Settings > Secrets and variables > Actions`):

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `GHCR_USER` | GitHub username | `johndoe` |
| `GHCR_PAT` | Personal Access Token | `ghp_xxxxxxxxxxxx` |
| `REPO_USER` | Repository owner username | `johndoe` |
| `SSH_HOST` | Ubuntu server IP | `192.168.1.100` |
| `SSH_USER` | Server username | `ubuntu` |
| `SSH_PRIVATE_KEY` | SSH private key | `-----BEGIN OPENSSH PRIVATE KEY-----...` |

## 🏥 Health Check Endpoint

The deployment relies on a health check endpoint in your FastAPI application:

```python
@app.get("/health")
async def healthcheck():
    return {
        "status": "healthy server",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "simple-fastapi-server"
    }
```

**Expected Response:**
```json
{
  "status": "healthy server",
  "timestamp": "2026-03-13T10:30:45.123456",
  "service": "simple-fastapi-server"
}
```

## 🚦 Deployment Flow Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Code Push     │───▶│  GitHub Actions  │───▶│   Build Image   │
│   (main/staging)│    │     Triggered    │    │   Push to GHCR  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  SSH to Server  │◀───│  Login to GHCR   │◀───│   Pull Image    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Start Test      │───▶│  Health Check    │───▶│ Deploy Success? │
│ Container :8080 │    │  /health         │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                    ┌────────────────────┼────────────────────┐
                                    ▼                    ▼                    ▼
                            ┌───────────────┐    ┌──────────────┐    ┌──────────────┐
                            │   SUCCESS     │    │    FAILURE   │    │   CLEANUP    │
                            │ Replace Prod  │    │  Keep Old    │    │ Remove Old   │
                            │ Container     │    │  Container   │    │   Images     │
                            │ Port :8005    │    │  Log Errors  │    │              │
                            └───────────────┘    └──────────────┘    └──────────────┘
```

## 🛠️ Troubleshooting Guide

### **Common Issues and Solutions**

#### **1. Authentication Failures**
```
Error: denied: permission_denied
```
**Solution:**
- Verify `GHCR_PAT` has `packages:write` scope
- Check `GHCR_USER` matches your GitHub username
- Ensure PAT hasn't expired

#### **2. SSH Connection Issues**
```
Error: ssh: connect to host X.X.X.X port 22: Connection refused
```
**Solution:**
- Verify `SSH_HOST` IP address is correct
- Check SSH service is running on server: `sudo systemctl status ssh`
- Validate `SSH_PRIVATE_KEY` format includes headers/footers
- Test SSH connection manually: `ssh -i key user@host`

#### **3. Health Check Failures**
```
Healthcheck failed. Keeping old container.
```
**Solution:**
- Check application logs: `docker logs fastapi_healthcheck`
- Verify `/health` endpoint is accessible
- Ensure container port mapping is correct (8080:8005)
- Check if application takes longer to start (increase sleep time)

#### **4. Port Conflicts**
```
Error: port is already allocated
```
**Solution:**
- Check for existing containers: `docker ps`
- Stop conflicting containers: `docker stop <container>`
- Verify port availability: `netstat -tulpn | grep :8005`

#### **5. Image Pull Failures**
```
Error: pull access denied for ghcr.io/user/repo
```
**Solution:**
- Verify image exists in GHCR
- Check repository visibility settings
- Ensure GHCR authentication is working
- Validate image tag format

### **Debugging Commands**

```bash
# Check running containers
docker ps -a

# View container logs
docker logs fastapi_app
docker logs fastapi_healthcheck

# Test health endpoint manually
curl http://localhost:8005/health
curl http://localhost:8080/health

# Check Docker images
docker images | grep sample-fastapi

# Monitor deployment in real-time
docker logs -f fastapi_app

# Check system resources
df -h
docker system df
```

## 📊 Monitoring and Logging

### **GitHub Actions Logs**
- View workflow runs in GitHub repository
- Check individual step outputs
- Monitor build times and success rates

### **Server-Side Monitoring**
```bash
# Monitor container health
docker stats fastapi_app

# Check application logs
docker logs -f --tail 100 fastapi_app

# Monitor system resources
htop
df -h
```

### **Application Metrics**
- Health endpoint response times
- Container restart frequency
- Deployment success/failure rates
- Resource utilization trends

## 🔄 Workflow Optimization Tips

### **1. Build Performance**
- Use multi-stage Dockerfiles
- Leverage build caching (`cache-from/cache-to`)
- Minimize image layers
- Use `.dockerignore` to exclude unnecessary files

### **2. Security Best Practices**
- Use non-root containers
- Scan images for vulnerabilities
- Rotate secrets regularly
- Implement least-privilege access

### **3. Reliability Improvements**
- Add retry logic for network operations
- Implement proper error handling
- Use health checks with appropriate timeouts
- Monitor deployment metrics

### **4. Scalability Considerations**
- Use load balancers for multiple instances
- Implement horizontal scaling
- Consider container orchestration (Kubernetes)
- Plan for database migrations

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [SSH Action Documentation](https://github.com/appleboy/ssh-action)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)

## 🎯 Key Takeaways

1. **Blue-green deployment** ensures zero-downtime updates
2. **Health checks** validate deployments before going live
3. **Automated rollback** maintains service availability
4. **Container registry** provides reliable image distribution
5. **SSH automation** enables secure remote deployments
6. **Comprehensive logging** aids in troubleshooting
7. **Secret management** maintains security best practices
