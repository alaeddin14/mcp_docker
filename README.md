# Weather MCP Server

This is a Model Context Protocol (MCP) server that provides weather forecast and alerts data via a containerized service. It uses the National Weather Service (NWS) API to fetch real-time weather information and exposes it through Server-Sent Events (SSE).

## Features

- Get weather forecasts for any location by latitude/longitude
- Get active weather alerts for any US state
- Containerized using Docker for easy deployment
- Supports Server-Sent Events (SSE) for client communication
- Configurable via environment variables

## Setup and Running

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for running the client)
- curl (for testing connectivity)

### Building and Running the Container

There are multiple ways to build and run the container:

#### Option 1: Using the helper script

```bash
# Build the image
./run.sh --build

# Run the container
./run.sh --run

# Or run in detached mode
./run.sh --run --detached

# Stop the container
./run.sh --stop
```

#### Option 2: Using Docker Compose directly

```bash
# Build and start
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop the container
docker-compose down
```

The server will be available at http://localhost:8585/sse

### Testing with the Client

A test client is provided to verify the MCP server is working correctly:

1. Install the required dependencies:

```bash
pip install "mcp[cli]" httpx
```

2. Run the test client:

```bash
python test_client.py
```

The client will:
- Connect to the MCP server using SSE
- List available tools
- Get a weather forecast for New York City
- Get weather alerts for California

## Available Tools

### get_forecast

Get weather forecasts for a location.

Parameters:
- `latitude` (float): Latitude of the location
- `longitude` (float): Longitude of the location

### get_alerts

Get active weather alerts for a US state.

Parameters:
- `state` (string): Two-letter US state code (e.g., 'CA' for California)

## Configuration

The server can be configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| HOST | The host address to bind to | 0.0.0.0 |
| PORT | The port to listen on | 8585 |
| USER_AGENT | User agent for NWS API requests | weather-app/1.0 |

You can also create a `.env` file based on `.env.example` to set these variables.

## Development

To modify the weather service and see changes without rebuilding:

1. Uncomment the volume mount in `docker-compose.yml`:
   ```yaml
   volumes:
     - .:/app
   ```

2. Restart the container:
   ```bash
   docker-compose restart
   ```

## Testing Connectivity

To test if the server is running correctly:

```bash
# Check if the SSE endpoint is available
curl -i http://localhost:8585/sse

# You should see a response with:
# Content-Type: text/event-stream
```

## Technical Details

- The MCP server uses FastMCP from the Model Context Protocol Python SDK
- The server is exposed via SSE transport on port 8585
- The container is based on Python 3.11 slim image
- Server-side events (SSE) allow real-time communication with clients
- The server exposes weather data from the National Weather Service API