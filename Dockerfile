# syntax=docker/dockerfile:1
FROM --platform=$TARGETPLATFORM python:3.10-slim

WORKDIR /app

# Copy source and install
COPY __init__.py __main__.py ./
COPY src/ ./src/
COPY pyproject.toml README.md ./

# Install dependencies and package
RUN pip install . && \
    rm -rf /var/lib/apt/lists/*

# Set Python path so 'python -m mcp4agent' works
ENV PYTHONPATH=/app

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose MCP ports
EXPOSE 8080 8081

# Run the MCP server
CMD ["python", "-m", "mcp4agent"]
