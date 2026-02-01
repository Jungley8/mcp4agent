FROM python:3.10-slim

WORKDIR /app

# Layer 1: Install dependencies first (for caching)
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir -e . && \
    rm -rf /var/lib/apt/lists/*

# Layer 2: Copy source code (rebuilds only when code changes)
COPY src/ ./src/

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Environment variables
ENV PYTHONPATH=/app
ENV WECHAT_TOKEN_CACHE_DIR=/app/.cache

# Expose MCP default port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.connect(('localhost', 8080)); s.close()" || exit 1

# Run the MCP server
CMD ["python", "-m", "wechat_mcp"]
