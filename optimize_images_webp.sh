#!/bin/bash

# Image Optimization Script - Convert large PNGs to optimized WebP
echo "Starting image optimization..."

# Create optimized versions directory
mkdir -p static/assets/img/optimized

# Function to convert and optimize images
optimize_image() {
    local input="$1"
    local output="$2"
    local quality="$3"
    
    if [ -f "$input" ]; then
        echo "Optimizing: $input -> $output"
        # Convert to WebP with specified quality
        cwebp -q "$quality" -m 6 -mt "$input" -o "$output"
        
        # Show size comparison
        original_size=$(stat -c%s "$input")
        new_size=$(stat -c%s "$output")
        savings=$((original_size - new_size))
        savings_percent=$((savings * 100 / original_size))
        
        echo "  Original: $(numfmt --to=iec-i --suffix=B $original_size)"
        echo "  Optimized: $(numfmt --to=iec-i --suffix=B $new_size)"
        echo "  Savings: $savings_percent%"
        echo ""
    fi
}

# Check if cwebp is installed
if ! command -v cwebp &> /dev/null; then
    echo "Installing webp tools..."
    sudo apt-get update
    sudo apt-get install -y webp
fi

# Optimize service images (largest files)
echo "=== Optimizing Service Images ==="
optimize_image "static/assets/img/service/service1.png" "static/assets/img/service/service1.webp" 80
optimize_image "static/assets/img/service/service2.png" "static/assets/img/service/service2.webp" 80
optimize_image "static/assets/img/service/service3.png" "static/assets/img/service/service3.webp" 80

# Optimize facility image
echo "=== Optimizing Facility Images ==="
optimize_image "static/assets/img/home/facility_1.png" "static/assets/img/home/facility_1.webp" 85

# Optimize doctor image
echo "=== Optimizing Doctor Images ==="
optimize_image "static/assets/img/doctor/atika.png" "static/assets/img/doctor/atika.webp" 85

# Create responsive versions for hero images if they don't exist as WebP
echo "=== Creating WebP versions of hero images ==="
if [ -f "static/assets/img/hero_section/mind_resized_1000x563.png" ]; then
    optimize_image "static/assets/img/hero_section/mind_resized_1000x563.png" "static/assets/img/hero_section/mind_resized_1000x563.webp" 85
fi

if [ -f "static/assets/img/hero_section/mind_resized_800x450.png" ]; then
    optimize_image "static/assets/img/hero_section/mind_resized_800x450.png" "static/assets/img/hero_section/mind_resized_800x450.webp" 85
fi

if [ -f "static/assets/img/hero_section/mind_resized_600x338.png" ]; then
    optimize_image "static/assets/img/hero_section/mind_resized_600x338.png" "static/assets/img/hero_section/mind_resized_600x338.webp" 85
fi

# Optimize logo to modern formats
echo "=== Optimizing Logo ==="
optimize_image "static/assets/img/logo.png" "static/assets/img/logo.webp" 90

echo "Image optimization complete!"
echo "Remember to update your templates to use the new .webp files"
