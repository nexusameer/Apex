#!/bin/bash

# Image Optimization Script for Mind Relief Clinic
# This script optimizes large JPEG images to improve website performance

echo "🔧 Optimizing large doctor images for better performance..."

# Navigate to the doctor images directory
cd /home/nexus/projects/apex/static/assets/img/doctor/

# Check if imagemagick is installed
if ! command -v convert &> /dev/null; then
    echo "⚠️  ImageMagick not found. Installing..."
    sudo apt-get update && sudo apt-get install -y imagemagick
fi

# Create backup directory
mkdir -p originals

# Optimize large images
for img in *.jpeg *.jpg; do
    if [ -f "$img" ]; then
        filesize=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img")
        # If file is larger than 50KB (51200 bytes)
        if [ "$filesize" -gt 51200 ]; then
            echo "📸 Optimizing $img ($(($filesize/1024))KB)"
            
            # Backup original
            cp "$img" "originals/$img"
            
            # Optimize: resize to max 800px width, 85% quality, progressive JPEG
            convert "$img" -resize "800x800>" -quality 85 -interlace Plane "$img"
            
            newsize=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img")
            echo "✅ Reduced from $(($filesize/1024))KB to $(($newsize/1024))KB"
        fi
    fi
done

echo "🎉 Image optimization complete!"
