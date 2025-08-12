#!/bin/bash

# Docker Space Management Script
echo "=== Docker Space Cleanup Utility ==="

# Function to show current docker usage
show_usage() {
    echo "Current Docker disk usage:"
    docker system df
    echo ""
    echo "Detailed breakdown:"
    docker system df -v
    echo ""
}

# Function for aggressive cleanup
aggressive_cleanup() {
    echo "🧹 Performing aggressive cleanup..."
    
    # Stop and remove all stopped containers
    echo "Removing stopped containers..."
    docker container prune -f
    
    # Remove unused networks
    echo "Removing unused networks..."
    docker network prune -f
    
    # Remove unused volumes
    echo "Removing unused volumes..."
    docker volume prune -f
    
    # Remove unused images
    echo "Removing unused images..."
    docker image prune -a -f
    
    # Remove build cache
    echo "Removing build cache..."
    docker builder prune -a -f
    
    echo "✅ Aggressive cleanup completed"
}

# Function for safe cleanup (keeps running containers and recent images)
safe_cleanup() {
    echo "🧼 Performing safe cleanup..."
    
    # Remove stopped containers only
    echo "Removing stopped containers..."
    docker container prune -f
    
    # Remove dangling images only
    echo "Removing dangling images..."
    docker image prune -f
    
    # Remove unused networks
    echo "Removing unused networks..."
    docker network prune -f
    
    # Remove unused volumes
    echo "Removing unused volumes..."
    docker volume prune -f
    
    echo "✅ Safe cleanup completed"
}

# Function to cleanup specific to apex project
apex_cleanup() {
    echo "🎯 Cleaning up old apex project images..."
    
    # Keep only latest 2 apex images
    old_images=$(docker images nexusameer/apex --format "{{.ID}} {{.Tag}}" | tail -n +3 | awk '{print $1}')
    
    if [ -n "$old_images" ]; then
        echo "Removing old apex images:"
        echo "$old_images"
        echo "$old_images" | xargs docker rmi -f 2>/dev/null || true
    else
        echo "No old apex images to remove"
    fi
    
    echo "✅ Apex cleanup completed"
}

# Main menu
main() {
    echo "Docker cleanup options:"
    echo "1. Show current usage"
    echo "2. Safe cleanup (recommended)"
    echo "3. Apex project cleanup"
    echo "4. Aggressive cleanup (removes everything unused)"
    echo "5. All cleanups"
    echo ""
    
    # If running with argument, use it
    if [ $# -eq 1 ]; then
        choice=$1
    else
        echo -n "Choose option (1-5): "
        read choice
    fi
    
    case $choice in
        1)
            show_usage
            ;;
        2)
            show_usage
            safe_cleanup
            echo ""
            show_usage
            ;;
        3)
            show_usage
            apex_cleanup
            echo ""
            show_usage
            ;;
        4)
            show_usage
            echo "⚠️  WARNING: This will remove ALL unused Docker resources!"
            if [ $# -eq 0 ]; then
                echo -n "Are you sure? (y/N): "
                read confirm
                if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
                    echo "Cancelled"
                    exit 0
                fi
            fi
            aggressive_cleanup
            echo ""
            show_usage
            ;;
        5)
            show_usage
            safe_cleanup
            apex_cleanup
            echo ""
            show_usage
            ;;
        *)
            echo "Invalid option"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
