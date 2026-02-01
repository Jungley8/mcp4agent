# syntax=docker/dockerfile:1
FROM --platform=$TARGETPLATFORM python:3.10-slim

WORKDIR /app

COPY pyproject.toml README.md ./
RUN mkdir -p src/mcp4agent && touch src/mcp4agent/__init__.py
RUN pip install --no-cache-dir -e .

# 覆盖源代码
COPY src/ ./src/

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
