# 🚀 Deployment Troubleshooting Guide

## Common Issues and Solutions

### 1. Port Already in Use Error
**Error**: `Bind for 0.0.0.0:8001 failed: port is already allocated`

**Solution**: Use the improved deploy.sh script which handles this automatically:

```bash
# Manual fix if needed:
# Find containers using port 8001
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}" | grep ":8001"

# Stop the specific container
docker stop gallant_chatterjee  # or whatever the container name is
docker rm gallant_chatterjee

# Then run deployment
./deploy.sh
```

### 2. Container Starts but Website Not Accessible
**Check these steps**:

```bash
# 1. Check if container is running
docker ps | grep apex

# 2. Check container logs
docker logs apex

# 3. Check if port is accessible
curl http://localhost:8001

# 4. Check container network
docker port apex
```

### 3. Database Connection Issues
**Common causes**:
- Missing environment variables
- Database not running
- Wrong database credentials

**Check**:
```bash
# Verify environment variables are set
docker exec apex env | grep DB_

# Check if PostgreSQL is running
docker ps | grep postgres

# Test database connection from container
docker exec apex python manage.py dbshell
```

### 4. Static Files Not Loading
**Solution**: Make sure static files are collected:

```bash
# Enter container and collect static files
docker exec apex python manage.py collectstatic --noinput

# Or rebuild image with static files included
```

### 5. Memory/Disk Space Issues
**Use the cleanup script**:

```bash
# Download cleanup script
curl -sSL https://raw.githubusercontent.com/nexusameer/Apex/main/docker-cleanup.sh -o docker-cleanup.sh
chmod +x docker-cleanup.sh

# Run safe cleanup
./docker-cleanup.sh 2

# Or aggressive cleanup (removes everything unused)
./docker-cleanup.sh 4
```

## Deployment Commands

### Quick Deployment
```bash
cd /root
./deploy.sh
```

### Manual Deployment Steps
```bash
# 1. Stop existing containers
docker stop $(docker ps -q --filter "ancestor=nexusameer/apex")
docker rm $(docker ps -aq --filter "ancestor=nexusameer/apex")

# 2. Pull latest image
docker pull nexusameer/apex:latest

# 3. Run new container
docker run -d --restart always -p 8001:8001 \
  --name apex \
  -e DB_HOST="$DB_HOST" \
  -e DB_NAME="$DB_NAME" \
  -e DB_USER="$DB_USER" \
  -e DB_PASSWORD="$DB_PASSWORD" \
  -e CLOUDINARY_CLOUD_NAME="$CLOUDINARY_CLOUD_NAME" \
  -e CLOUDINARY_API_KEY="$CLOUDINARY_API_KEY" \
  -e CLOUDINARY_API_SECRET="$CLOUDINARY_API_SECRET" \
  nexusameer/apex:latest
```

### Health Check Commands
```bash
# Check container status
docker ps | grep apex

# Check container health
docker logs apex --tail 50

# Check resource usage
docker stats apex --no-stream

# Test website response
curl -I http://localhost:8001
```

### Rollback to Previous Version
```bash
# List available images
docker images nexusameer/apex

# Stop current container
docker stop apex && docker rm apex

# Run previous image (replace IMAGE_ID with actual ID)
docker run -d --restart always -p 8001:8001 \
  --name apex \
  -e DB_HOST="$DB_HOST" \
  [... other env vars ...] \
  IMAGE_ID
```

## Monitoring Commands

### Real-time Logs
```bash
# Follow container logs
docker logs -f apex

# Filter for errors
docker logs apex 2>&1 | grep -i error
```

### Performance Monitoring
```bash
# Container resource usage
docker stats apex

# Disk usage
docker system df

# Network connections
netstat -tlnp | grep :8001
```

## Environment Variables Check
Make sure these are set in ~/.bashrc:

```bash
export DB_HOST="134.199.213.29"
export DB_NAME="postgres"
export DB_USER="postgres"
export DB_PASSWORD="apexpassword"
export CLOUDINARY_CLOUD_NAME="your_cloud_name"
export CLOUDINARY_API_KEY="your_api_key"
export CLOUDINARY_API_SECRET="your_api_secret"
```

Reload with: `source ~/.bashrc`

## Emergency Procedures

### Complete Reset
```bash
# Stop all containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images (DANGEROUS - only if needed)
docker rmi $(docker images -q)

# Start fresh
docker pull nexusameer/apex:latest
./deploy.sh
```

### Database Reset (if needed)
```bash
# Backup first!
docker exec postgres14 pg_dump -U postgres postgres > backup.sql

# Reset database
docker exec postgres14 psql -U postgres -c "DROP DATABASE IF EXISTS postgres;"
docker exec postgres14 psql -U postgres -c "CREATE DATABASE postgres;"

# Run migrations
docker exec apex python manage.py migrate
```

## Contact Information
- Repository: https://github.com/nexusameer/Apex
- Docker Hub: https://hub.docker.com/r/nexusameer/apex
