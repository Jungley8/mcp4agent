# syntax=docker/dockerfile:1
# ============================================
# MCP4Agent - Multi-package MCP Server
# Built with BuildKit for optimal caching
# ============================================

# -----------------------
# Base Image
# -----------------------
FROM --platform=$TARGETPLATFORM python:3.10-slim AS base

# Set Python encoding
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=0 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# -----------------------
# Dependencies Stage
# -----------------------
FROM base AS deps

# Copy only dependency files first (for better caching)
COPY pyproject.toml README.md .

# Install dependencies with BuildKit cache mount
# This creates a persistent pip cache across builds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install . && \
    rm -rf /var/lib/apt/lists/*

# -----------------------
# Builder Stage (for editable install if needed)
# -----------------------
FROM base AS builder

# Copy dependency installation from deps stage
COPY --from=deps /root/.cache/pip /root/.cache/pip
COPY --from=deps /app /app

# Copy source code
COPY src/ ./src/

# Reinstall in editable mode for development
RUN pip install -e . --no-deps && \
    rm -rf /root/.cache/pip

# -----------------------
# Production Stage
# -----------------------
FROM base AS production

# Copy from deps (installed dependencies)
COPY --from=deps /root/.cache/pip /root/.cache/pip
COPY --from=deps /app /usr/local

# Copy source code
COPY src/ ./src/

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Environment variables
ENV PYTHONPATH=/app \
    WECHAT_TOKEN_CACHE_DIR=/app/.cache \
    PIP_CACHE_DIR=/root/.cache/pip

# Expose MCP ports
EXPOSE 8080 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.connect(('localhost', 8080)); s.close()" || exit 1

# Run the MCP server (all services)
CMD ["python", "-m", "mcp4agent"]
