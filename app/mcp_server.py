\
# filepath: /home/alaeddin/MCP/mcp_docker_test1/app/mcp_server.py
"""
Centralized MCP server instance.
"""
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
# The 'name' can be configured via environment variable or a default.
# Host and port for the server to listen on will be handled by mcp.run() in main.py

# Get port from environment or use default
mcp_name=os.environ.get("MCP_SERVER_NAME", "my-mcp-application")
mcp_port = int(os.environ.get("PORT", 8585))
mcp_host = os.environ.get("HOST", "0.0.0.0")
mcp = FastMCP(mcp_name, host=mcp_host, port=mcp_port)
# mcp = FastMCP(name=os.environ.get("MCP_SERVER_NAME", "my-mcp-application"))

# You can add any other server-wide configurations here if needed in the future.
