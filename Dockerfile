# syntax=docker/dockerfile:1
FROM --platform=$TARGETPLATFORM python:3.10-slim

WORKDIR /app

# Install Chinese fonts and set UTF-8 encoding
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-noto-cjk \
    fonts-wqy-microhei \
    fonts-wqy-zenhei \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

COPY pyproject.toml README.md ./
RUN mkdir -p src/mcp4agent && touch src/mcp4agent/__init__.py
RUN pip install --no-cache-dir -e .

# 覆盖源代码
COPY src/ ./src/

# Set Python path and UTF-8 encoding
ENV PYTHONPATH=/app \
    LANG=C.UTF-8 \
    PYTHONIOENCODING=utf-8 \
    PYTHONUNBUFFERED=1

# Create cache directory and non-root user
RUN mkdir -p /app/.cache && \
    useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose MCP ports
EXPOSE 8080 8081

# Run the MCP server
CMD ["python", "-m", "mcp4agent"]
