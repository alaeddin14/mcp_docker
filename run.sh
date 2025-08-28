#!/bin/bash
# Helper script to build and run the MCP weather server docker container
# filepath: /home/alaeddin/MCP/mcp_docker_test1/scripts/run.sh

set -e  # Exit on error

# Display help message
show_help() {
  echo "Usage: ./run.sh [OPTIONS]"
  echo ""
  echo "Options:"
  echo "  -b, --build       Build the Docker image"
  echo "  -r, --run         Run the container (default if no options provided)"
  echo "  -d, --detached    Run in detached mode"
  echo "  -s, --stop        Stop the running container"
  echo "  -h, --help        Show this help message"
}

# Default action
ACTION="run"
DETACHED=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -b|--build)
      ACTION="build"
      shift
      ;;
    -r|--run)
      ACTION="run"
      shift
      ;;
    -d|--detached)
      DETACHED="-d"
      shift
      ;;
    -s|--stop)
      ACTION="stop"
      shift
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

# Execute the selected action
case "$ACTION" in
  build)
    echo "Building Docker image..."
    docker compose -f docker/docker-compose.yml build # Changed path to docker-compose.yml
    ;;
  run)
    echo "Running Docker container..."
    if [ -n "$DETACHED" ]; then
      echo "Running in detached mode..."
      docker compose -f docker/docker-compose.yml up $DETACHED # Changed path to docker-compose.yml
    else
      docker compose -f docker/docker-compose.yml up # Changed path to docker-compose.yml
    fi
    ;;
  stop)
    echo "Stopping Docker container..."
    docker compose -f docker/docker-compose.yml down # Changed path to docker-compose.yml
    ;;
esac
