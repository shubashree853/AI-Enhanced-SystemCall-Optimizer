#!/bin/bash
# ============================================================================
# Quick Script to Build and Push Docker Image
# ============================================================================
# This script helps you quickly build and push your Docker image to Docker Hub
# Usage: ./docker-build-and-push.sh [your-dockerhub-username] [image-name] [tag]
# ============================================================================

# Set default values
DOCKERHUB_USERNAME=${1:-"your-dockerhub-username"}
IMAGE_NAME=${2:-"syscall-optimizer"}
TAG=${3:-"latest"}

# Full image name
FULL_IMAGE_NAME="${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${TAG}"

echo "=========================================="
echo "Docker Build and Push Script"
echo "=========================================="
echo "Docker Hub Username: $DOCKERHUB_USERNAME"
echo "Image Name: $IMAGE_NAME"
echo "Tag: $TAG"
echo "Full Image: $FULL_IMAGE_NAME"
echo "=========================================="
echo ""

# Step 1: Build the image
echo "Step 1: Building Docker image..."
docker build -t "$FULL_IMAGE_NAME" .
if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi
echo "✅ Build successful!"
echo ""

# Step 2: Login to Docker Hub
echo "Step 2: Logging in to Docker Hub..."
docker login
if [ $? -ne 0 ]; then
    echo "❌ Login failed!"
    exit 1
fi
echo "✅ Login successful!"
echo ""

# Step 3: Push the image
echo "Step 3: Pushing image to Docker Hub..."
docker push "$FULL_IMAGE_NAME"
if [ $? -ne 0 ]; then
    echo "❌ Push failed!"
    exit 1
fi
echo "✅ Push successful!"
echo ""

# Step 4: Create and push latest tag (if not already latest)
if [ "$TAG" != "latest" ]; then
    echo "Step 4: Tagging as latest..."
    docker tag "$FULL_IMAGE_NAME" "${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest"
    docker push "${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest"
    echo "✅ Latest tag pushed!"
    echo ""
fi

echo "=========================================="
echo "✅ All done! Your image is available at:"
echo "   docker pull $FULL_IMAGE_NAME"
echo "=========================================="

