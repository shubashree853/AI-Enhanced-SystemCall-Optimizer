# ============================================================================
# Quick Script to Build and Push Docker Image (PowerShell)
# ============================================================================
# This script helps you quickly build and push your Docker image to Docker Hub
# Usage: .\docker-build-and-push.ps1 [your-dockerhub-username] [image-name] [tag]
# ============================================================================

param(
    [string]$DockerHubUsername = "your-dockerhub-username",
    [string]$ImageName = "syscall-optimizer",
    [string]$Tag = "latest"
)

# Full image name
$FullImageName = "${DockerHubUsername}/${ImageName}:${Tag}"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Docker Build and Push Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Docker Hub Username: $DockerHubUsername"
Write-Host "Image Name: $ImageName"
Write-Host "Tag: $Tag"
Write-Host "Full Image: $FullImageName"
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Build the image
Write-Host "Step 1: Building Docker image..." -ForegroundColor Yellow
docker build -t $FullImageName .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Build successful!" -ForegroundColor Green
Write-Host ""

# Step 2: Login to Docker Hub
Write-Host "Step 2: Logging in to Docker Hub..." -ForegroundColor Yellow
docker login
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Login failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Login successful!" -ForegroundColor Green
Write-Host ""

# Step 3: Push the image
Write-Host "Step 3: Pushing image to Docker Hub..." -ForegroundColor Yellow
docker push $FullImageName
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Push failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Push successful!" -ForegroundColor Green
Write-Host ""

# Step 4: Create and push latest tag (if not already latest)
if ($Tag -ne "latest") {
    Write-Host "Step 4: Tagging as latest..." -ForegroundColor Yellow
    $LatestTag = "${DockerHubUsername}/${ImageName}:latest"
    docker tag $FullImageName $LatestTag
    docker push $LatestTag
    Write-Host "✅ Latest tag pushed!" -ForegroundColor Green
    Write-Host ""
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ All done! Your image is available at:" -ForegroundColor Green
Write-Host "   docker pull $FullImageName" -ForegroundColor White
Write-Host "==========================================" -ForegroundColor Cyan

