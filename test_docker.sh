#!/bin/bash

# Test Docker build locally
echo "🐳 Testing Docker build locally..."

# Build the image
echo "Building Docker image..."
docker build -t ai-job-assistant-test .

if [ $? -eq 0 ]; then
    echo "✅ Docker build successful!"
    
    # Test run (optional)
    echo "🚀 Starting container for testing..."
    docker run -d -p 10000:10000 \
        -e GROQ_API_KEY=test_key \
        --name ai-job-test \
        ai-job-assistant-test
    
    # Wait a moment for startup
    sleep 5
    
    # Test health endpoint
    echo "🔍 Testing health endpoint..."
    curl -f http://localhost:10000/health
    
    if [ $? -eq 0 ]; then
        echo "✅ Health check passed!"
    else
        echo "❌ Health check failed"
    fi
    
    # Cleanup
    echo "🧹 Cleaning up..."
    docker stop ai-job-test
    docker rm ai-job-test
    
else
    echo "❌ Docker build failed!"
    exit 1
fi

echo "🎉 Local Docker test completed!"