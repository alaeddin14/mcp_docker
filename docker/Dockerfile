# filepath: /home/alaeddin/MCP/mcp_docker_test1/docker/Dockerfile
FROM python:3.13-alpine

WORKDIR /app

# Install system dependencies
RUN apk update && apk add --no-cache build-base

# Copy requirements files
COPY pyproject.toml uv.lock /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip uv \
    && uv pip install --system -e . \
    && pip install --no-cache-dir "mcp[cli]" httpx uvicorn

# Copy application code
COPY app /app/app
COPY version.py /app/version.py
# COPY .env /app/.env 


# Expose port for SSE transport
EXPOSE 8585

# Run the MCP server using main.py
WORKDIR /app
# ... other instructions ...
CMD ["python", "-m", "app.main"]
