# Docker Deployment Guide

## Using the Published Docker Image

The wechat-mcp project publishes Docker images to GitHub Container Registry (GHCR).

### Pulling the Image

```bash
# Replace with your actual GitHub username
export GHCR_USERNAME="your-github-username"

# Pull the latest image
docker pull ghcr.io/$GHCR_USERNAME/wechat-mcp:latest

# Pull a specific version
docker pull ghcr.io/$GHCR_USERNAME/wechat-mcp:v1.0.0
```

### Running the Container

```bash
# Basic run
docker run -d \
  --name wechat-mcp \
  -p 8080:8080 \
  ghcr.io/$GHCR_USERNAME/wechat-mcp:latest

# With environment variables
docker run -d \
  --name wechat-mcp \
  -p 8080:8080 \
  -e WECHAT_TOKEN_CACHE_DIR=/app/.cache \
  -v $(pwd)/data:/app/.cache \
  ghcr.io/$GHCR_USERNAME/wechat-mcp:latest
```

### Using Docker Compose

```yaml
version: '3.8'

services:
  wechat-mcp:
    image: ghcr.io/$GHCR_USERNAME/wechat-mcp:latest
    container_name: wechat-mcp
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/.cache
    environment:
      - WECHAT_TOKEN_CACHE_DIR=/app/.cache
    restart: unless-stopped
```

### Image Tags

- `latest` - Most recent stable release
- `vX.Y.Z` - Specific version tag
- `sha-xxxxxxxx` - Commit-specific build

### Multi-Platform Support

The images are built for:
- `linux/amd64` - x86_64 systems
- `linux/arm64` - ARM64 systems (Apple Silicon, Raspberry Pi)
