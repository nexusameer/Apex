#!/bin/bash

echo "=== Mind Relief Clinic Deployment Script ==="
echo "Starting deployment process..."

# Load environment variables from ~/.bashrc
source ~/.bashrc

# Function to stop and remove containers using port 8001
cleanup_port_8001() {
    echo "Checking for containers using port 8001..."
    
    # Find containers using port 8001 (both by name and port mapping)
    port_containers=$(docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}" | grep ":8001->" | awk '{print $1}')
    apex_containers=$(docker ps -aq --filter "name=apex")
    
    # Combine and deduplicate container IDs
    all_containers=$(echo -e "$port_containers\n$apex_containers" | sort -u | grep -v '^$')
    
    if [ -n "$all_containers" ]; then
        echo "Found containers to stop:"
        docker ps --filter "id=$(echo $all_containers | tr ' ' '\n' | head -1)" --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}\t{{.Status}}"
        
        echo "Stopping and removing existing containers..."
        for container in $all_containers; do
            echo "Stopping container: $container"
            docker stop "$container" 2>/dev/null || true
            echo "Removing container: $container"
            docker rm "$container" 2>/dev/null || true
        done
        echo "✅ Old containers cleaned up"
    else
        echo "No existing containers found using port 8001"
    fi
}

# Function to cleanup old images
cleanup_old_images() {
    echo "Cleaning up old images..."
    
    # Remove dangling images (untagged)
    dangling=$(docker images -f "dangling=true" -q)
    if [ -n "$dangling" ]; then
        echo "Removing dangling images..."
        docker rmi $dangling 2>/dev/null || true
    fi
    
    # Keep only the latest 2 versions of nexusameer/apex
    echo "Cleaning up old nexusameer/apex images..."
    old_apex_images=$(docker images nexusameer/apex --format "{{.ID}}" | tail -n +3)
    if [ -n "$old_apex_images" ]; then
        echo "Removing old apex images..."
        docker rmi $old_apex_images 2>/dev/null || true
    fi
    
    # Remove unused images (optional - be careful with this)
    echo "Removing unused images..."
    docker image prune -f
    
    echo "✅ Image cleanup completed"
}

# Function to show disk usage
show_disk_usage() {
    echo "=== Docker Disk Usage ==="
    docker system df
    echo ""
}

# Main deployment process
main() {
    echo "Starting deployment at $(date)"
    
    # Show initial disk usage
    show_disk_usage
    
    # Cleanup existing containers
    cleanup_port_8001
    
    # Pull latest image
    echo "Pulling latest image..."
    docker pull nexusameer/apex:latest
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to pull latest image"
        exit 1
    fi
    echo "✅ Latest image pulled successfully"
    
    # Run the new container
    echo "Starting new container..."
    docker run -d --restart always -p 8001:8001 \
      --name apex \
      -v /root/apex_media:/app/media \
      -e DB_HOST="$DB_HOST" \
      -e DB_NAME="$DB_NAME" \
      -e DB_USER="$DB_USER" \
      -e DB_PASSWORD="$DB_PASSWORD" \
      -e CLOUDINARY_CLOUD_NAME="$CLOUDINARY_CLOUD_NAME" \
      -e CLOUDINARY_API_KEY="$CLOUDINARY_API_KEY" \
      -e CLOUDINARY_API_SECRET="$CLOUDINARY_API_SECRET" \
      nexusameer/apex:latest
    
    if [ $? -eq 0 ]; then
        echo "✅ Container started successfully"
        
        # Wait a moment for container to initialize
        sleep 5
        
        # Check if container is running
        if docker ps | grep -q "apex"; then
            echo "✅ Container is running and healthy"
            
            # Cleanup old images after successful deployment
            cleanup_old_images
            
            # Show final status
            echo ""
            echo "=== Deployment Status ==="
            docker ps --filter "name=apex" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
            echo ""
            echo "🚀 Deployment completed successfully!"
            echo "Website should be accessible at: http://your-server:8001"
            
        else
            echo "❌ Container failed to start properly"
            echo "Container logs:"
            docker logs apex
            exit 1
        fi
    else
        echo "❌ Failed to start container"
        exit 1
    fi
    
    # Show final disk usage
    show_disk_usage
}

# Handle script interruption
trap 'echo "Deployment interrupted"; exit 1' INT TERM

# Run main function
main

echo "Deployment completed at $(date)"
