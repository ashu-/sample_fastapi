# 🎓 FastAPI Docker Deployment Demo Script

## Demo Agenda (45-60 minutes)

### Part 1: Introduction (10 minutes)
- **What we'll build**: Simple FastAPI server with health endpoint
- **What we'll learn**: Docker, GHCR, CI/CD, Blue-Green deployment
- **Why it matters**: Production deployment best practices

### Part 2: Local Development (10 minutes)

#### Step 1: Explore the FastAPI Application
```bash
# Show the main.py file
cat main.py

# Run locally with uv
uv run python main.py

# Test in another terminal
curl http://localhost:8000/health
```

**Teaching Points:**
- FastAPI basics and health endpoints
- Why health checks are crucial in production
- uv for modern Python dependency management

### Part 3: Docker Containerization (15 minutes)

#### Step 2: Understanding the Dockerfile
```bash
# Explain each section of the Dockerfile
cat Dockerfile
```

**Teaching Points:**
- Multi-stage builds for optimization
- Security: non-root user
- Health checks in containers
- Platform-specific builds (ARM64/AMD64)

#### Step 3: Build and Test Docker Image
```bash
# Build the Docker image
docker build -t fastapi-demo .

# Run the container
docker run -d --name fastapi-test -p 8000:8000 fastapi-demo

# Test the containerized app
curl http://localhost:8000/health

# Check container status
docker ps
docker logs fastapi-test

# Clean up
docker stop fastapi-test
docker rm fastapi-test
```

**Teaching Points:**
- Docker build process
- Container networking and port mapping
- Container lifecycle management
- Debugging with logs

#### Step 4: Docker Compose for Development
```bash
# Show docker-compose.yml
cat docker-compose.yml

# Run with docker-compose
docker-compose up --build

# Test in another terminal
curl http://localhost:8000/health

# Stop services
docker-compose down
```

**Teaching Points:**
- Docker Compose for multi-service applications
- Development vs production configurations
- Volume mounting for hot reload

### Part 4: GitHub Container Registry Setup (10 minutes)

#### Step 5: Understanding GHCR
**Teaching Points:**
- What is a container registry?
- Why use GHCR vs Docker Hub?
- Authentication and permissions

#### Step 6: GitHub Secrets Configuration
Show how to configure:
```
GHCR_USER          # GitHub username
GHCR_PAT           # Personal Access Token (packages:write)
SSH_HOST           # Ubuntu server IP
SSH_USER           # Ubuntu server username  
SSH_PRIVATE_KEY    # SSH private key
```

**Teaching Points:**
- Security best practices for secrets
- PAT scopes and permissions
- SSH key authentication

### Part 5: CI/CD Pipeline Deep Dive (15 minutes)

#### Step 7: GitHub Actions Workflow Analysis
```bash
# Explain the workflow file
cat .github/workflows/deploy.yml
```

**Teaching Points:**
- Trigger conditions (push to main/staging)
- Multi-platform builds with Buildx
- GHCR authentication and image pushing

#### Step 8: Blue-Green Deployment Strategy
Explain the deployment script section:

```bash
# The key deployment logic:
# 1. Pull new image
# 2. Run test container on different port
# 3. Health check validation
# 4. Swap containers if healthy
# 5. Rollback if unhealthy
```

**Teaching Points:**
- Zero-downtime deployments
- Risk mitigation with health checks
- Rollback strategies
- Container lifecycle in production

### Part 6: Live Deployment Demo (10 minutes)

#### Step 9: Trigger Deployment
```bash
# Make a small change to trigger deployment
echo "# Updated $(date)" >> README.md
git add .
git commit -m "Demo: trigger deployment"
git push origin main
```

#### Step 10: Monitor Deployment
- Watch GitHub Actions workflow execution
- Show GHCR package creation
- Monitor server deployment (if available)
- Test production endpoint

**Teaching Points:**
- Monitoring CI/CD pipelines
- Debugging deployment failures
- Production verification steps

### Part 7: Production Considerations (5 minutes)

#### Discussion Topics:
- **Scaling**: Load balancers, multiple instances
- **Monitoring**: Logs, metrics, alerts
- **Security**: Image scanning, secrets rotation
- **Backup**: Data persistence, disaster recovery
- **Performance**: Resource limits, optimization

### Part 8: Hands-on Exercise (Optional)

#### Challenge for Interns:
1. Fork the repository
2. Modify the health endpoint to include system info
3. Update the Dockerfile if needed
4. Configure their own GHCR deployment
5. Deploy their changes

#### Expected Learning Outcomes:
- Hands-on Docker experience
- Understanding of CI/CD pipelines
- Production deployment confidence
- Troubleshooting skills

## 🛠️ Troubleshooting Guide for Demo

### Common Issues During Demo:

1. **Docker build fails:**
   ```bash
   # Check Docker daemon
   docker version
   
   # Clear build cache
   docker builder prune
   ```

2. **Port already in use:**
   ```bash
   # Find and kill process
   lsof -i :8000
   kill <PID>
   ```

3. **GitHub Actions fails:**
   - Check secrets configuration
   - Verify PAT permissions
   - Review workflow logs

4. **Health check fails:**
   ```bash
   # Debug container
   docker exec -it <container> /bin/bash
   curl localhost:8000/health
   ```

## 📚 Additional Resources for Interns

- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Container Security Guide](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

## 🎯 Key Takeaways

By the end of this demo, interns should understand:
- How to containerize Python applications
- CI/CD pipeline design and implementation
- Production deployment strategies
- Container registry usage
- Security considerations in DevOps
- Monitoring and troubleshooting techniques
