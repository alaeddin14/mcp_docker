"""
Main entry point for the MCP Server.
This runs the server with SSE transport.
"""

import os
import logging
from .mcp_server import mcp # Import the shared mcp instance
# Import tool modules so they register with the mcp instance
from . import weather 
from . import google_maps
# To add more tools, create a new .py file (e.g., new_tools.py) in the 'app' directory,
# define your tools there using the same 'mcp' instance from '.mcp_server',
# and then import that module here, e.g.:
# from . import new_tools

def main():
    """Run the MCP server with SSE transport"""
    # Get port from environment or use default
    mcp_name = os.environ.get("MCP_SERVER_NAME", "my-mcp-application_main")
    mcp_port = int(os.environ.get("PORT", 8585))
    mcp_host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"Printing: Starting MCP Server '{mcp_name}' on {mcp_host}:{mcp_port}")

    
    # Run the server with SSE transport
    mcp.run(transport="sse")

if __name__ == "__main__":
    main()
