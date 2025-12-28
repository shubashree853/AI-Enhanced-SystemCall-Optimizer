# 🐳 Docker Guide - AI-Enhanced System Call Optimization

This guide will help you build, run, and push your Django application to Docker Hub.

---

## 📋 Prerequisites

Before you begin, make sure you have:

1. **Docker installed** on your system
   - Windows/Mac: Download from [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Linux: Install using your package manager
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install docker.io docker-compose
   ```

2. **Docker Hub account** (for pushing images)
   - Sign up at [hub.docker.com](https://hub.docker.com/signup)

3. **Verify Docker installation**
   ```bash
   docker --version
   docker-compose --version
   ```

---

## 🏗️ Building the Docker Image

### Method 1: Using Docker Build (Recommended for pushing to Docker Hub)

```bash
# Build the image
# -t flag tags the image with a name
# . means use current directory as build context
docker build -t syscall-optimizer:latest .

# Or with your Docker Hub username:
docker build -t your-dockerhub-username/syscall-optimizer:latest .
```

**Explanation:**
- `docker build`: Command to build an image
- `-t syscall-optimizer:latest`: Tags the image with name `syscall-optimizer` and tag `latest`
- `.`: Build context (current directory)

### Method 2: Using Docker Compose

```bash
# Build and start services
docker-compose up --build

# Or build without starting:
docker-compose build
```

---

## 🚀 Running the Container

### Method 1: Using Docker Run

```bash
# Run the container
docker run -d \
  --name syscall-optimizer \
  -p 8000:8000 \
  -e SECRET_KEY="your-secret-key-here" \
  -e GROQ_API_KEY="your-groq-api-key" \
  -v $(pwd)/media:/app/media \
  -v $(pwd)/db.sqlite3:/app/db.sqlite3 \
  syscall-optimizer:latest
```

**For Windows PowerShell:**
```powershell
docker run -d `
  --name syscall-optimizer `
  -p 8000:8000 `
  -e SECRET_KEY="your-secret-key-here" `
  -e GROQ_API_KEY="your-groq-api-key" `
  -v ${PWD}/media:/app/media `
  -v ${PWD}/db.sqlite3:/app/db.sqlite3 `
  syscall-optimizer:latest
```

**Explanation:**
- `-d`: Run in detached mode (background)
- `--name`: Give container a name
- `-p 8000:8000`: Map port 8000 from container to host
- `-e`: Set environment variables
- `-v`: Mount volumes for persistent data

### Method 2: Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access the application:**
- Open browser: `http://localhost:8000`

---

## 📤 Pushing to Docker Hub

### Step 1: Login to Docker Hub

```bash
docker login
```

Enter your Docker Hub username and password when prompted.

### Step 2: Tag Your Image

Tag your image with your Docker Hub username:

```bash
# Format: docker tag <local-image> <dockerhub-username>/<repository>:<tag>
docker tag syscall-optimizer:latest your-dockerhub-username/syscall-optimizer:latest

# You can also create version tags
docker tag syscall-optimizer:latest your-dockerhub-username/syscall-optimizer:v1.0.0
```

**Example:**
```bash
docker tag syscall-optimizer:latest nandanam/syscall-optimizer:latest
```

### Step 3: Push to Docker Hub

```bash
# Push the image
docker push your-dockerhub-username/syscall-optimizer:latest

# Push version tag
docker push your-dockerhub-username/syscall-optimizer:v1.0.0
```

**Example:**
```bash
docker push nandanam/syscall-optimizer:latest
```

### Step 4: Verify on Docker Hub

1. Go to [hub.docker.com](https://hub.docker.com)
2. Navigate to your repositories
3. You should see your `syscall-optimizer` repository

---

## 🔄 Complete Workflow Example

Here's a complete example from build to push:

```bash
# 1. Build the image
docker build -t nandanam/syscall-optimizer:latest .

# 2. Test locally (optional)
docker run -d -p 8000:8000 --name test-container nandanam/syscall-optimizer:latest
# Visit http://localhost:8000 to test
docker stop test-container
docker rm test-container

# 3. Login to Docker Hub
docker login

# 4. Push to Docker Hub
docker push nandanam/syscall-optimizer:latest

# 5. Create a version tag and push
docker tag nandanam/syscall-optimizer:latest nandanam/syscall-optimizer:v1.0.0
docker push nandanam/syscall-optimizer:v1.0.0
```

---

## 🎯 Pulling and Running Your Image

Once pushed, anyone can pull and run your image:

```bash
# Pull the image
docker pull your-dockerhub-username/syscall-optimizer:latest

# Run it
docker run -d \
  --name syscall-optimizer \
  -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e GROQ_API_KEY="your-api-key" \
  your-dockerhub-username/syscall-optimizer:latest
```

---

## 🔧 Useful Docker Commands

### View running containers
```bash
docker ps
```

### View all containers (including stopped)
```bash
docker ps -a
```

### View logs
```bash
docker logs syscall-optimizer
docker logs -f syscall-optimizer  # Follow logs
```

### Stop container
```bash
docker stop syscall-optimizer
```

### Start container
```bash
docker start syscall-optimizer
```

### Remove container
```bash
docker rm syscall-optimizer
```

### Remove image
```bash
docker rmi syscall-optimizer:latest
```

### Execute commands in running container
```bash
docker exec -it syscall-optimizer bash
docker exec -it syscall-optimizer python manage.py createsuperuser
```

### View image details
```bash
docker images
docker inspect syscall-optimizer:latest
```

---

## 🐛 Troubleshooting

### Issue: Port already in use
```bash
# Find what's using port 8000
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -i :8000

# Use a different port
docker run -p 8080:8000 syscall-optimizer:latest
```

### Issue: Permission denied
```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
# Log out and log back in
```

### Issue: Build fails
```bash
# Clean build (no cache)
docker build --no-cache -t syscall-optimizer:latest .

# View build logs
docker build -t syscall-optimizer:latest . 2>&1 | tee build.log
```

### Issue: Container exits immediately
```bash
# Check logs
docker logs syscall-optimizer

# Run interactively to see errors
docker run -it syscall-optimizer:latest bash
```

### Issue: Database migration errors
```bash
# Run migrations manually
docker exec -it syscall-optimizer python manage.py migrate
```

---

## 🔒 Security Best Practices

1. **Never commit secrets** to Docker images
   - Use environment variables or secrets management
   - Don't hardcode API keys in Dockerfile

2. **Use non-root user** (already configured in Dockerfile)

3. **Keep images updated**
   ```bash
   docker pull python:3.11-slim  # Update base image
   docker build -t syscall-optimizer:latest .
   ```

4. **Scan for vulnerabilities**
   ```bash
   docker scan syscall-optimizer:latest
   ```

5. **Use specific tags** instead of `latest` in production
   ```bash
   docker push your-username/syscall-optimizer:v1.0.0
   ```

---

## 📝 Environment Variables

Important environment variables you can set:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | Yes | None |
| `DEBUG` | Debug mode | No | False |
| `ALLOWED_HOSTS` | Allowed hostnames | No | localhost,127.0.0.1 |
| `GROQ_API_KEY` | Groq API key for AI features | No | None |
| `DATABASE_URL` | Database connection string | No | SQLite |

**Example:**
```bash
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY="django-insecure-your-secret-key" \
  -e DEBUG="False" \
  -e ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com" \
  -e GROQ_API_KEY="your-groq-api-key" \
  syscall-optimizer:latest
```

---

## 🚀 Production Deployment

For production, consider:

1. **Use a reverse proxy** (Nginx) in front of Gunicorn
2. **Use PostgreSQL** instead of SQLite
3. **Set up SSL/TLS** certificates
4. **Use Docker secrets** for sensitive data
5. **Set up monitoring** and logging
6. **Use orchestration** (Docker Swarm, Kubernetes)

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Gunicorn Documentation](https://gunicorn.org/)

---

## ✅ Quick Reference

```bash
# Build
docker build -t your-username/syscall-optimizer:latest .

# Run
docker run -d -p 8000:8000 your-username/syscall-optimizer:latest

# Login
docker login

# Push
docker push your-username/syscall-optimizer:latest

# Pull
docker pull your-username/syscall-optimizer:latest
```

---

**Happy Dockerizing! 🐳**

