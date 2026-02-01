# syntax=docker/dockerfile:1
FROM --platform=$TARGETPLATFORM python:3.10-slim

WORKDIR /app

# Copy source and install
COPY src/ ./src/
COPY pyproject.toml README.md ./

# Install in editable mode for reliable imports
RUN pip install -e . && \
    rm -rf /var/lib/apt/lists/*

# Set Python path
ENV PYTHONPATH=/app

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose MCP ports
EXPOSE 8080 8081

# Run the MCP server
CMD ["python", "-m", "mcp4agent"]
