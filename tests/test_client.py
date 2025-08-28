#!/usr/bin/env python3
"""
Example MCP client that connects to the weather MCP server via SSE.
This demonstrates how to connect to the containerized MCP server.
"""

import asyncio
import os
import sys
from mcp.client.sse import sse_client
from mcp import ClientSession

# Add the parent directory to the Python path to allow importing 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

async def main():
    # Get server URL from environment variable or use default
    server_host = os.environ.get("MCP_SERVER_HOST", "localhost")
    server_port = os.environ.get("MCP_SERVER_PORT", "8080") # This should match the port in docker-compose.yml
    server_url = f"http://{server_host}:{server_port}/sse"
    
    print(f"Connecting to MCP server at {server_url}...")
    
    async with sse_client(server_url) as (read_stream, write_stream):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            
            print("Connected to MCP server.")
            print("Server info:", session.server_info)
            
            print("\nAvailable tools:")
            tools = await session.list_tools()
            for tool in tools:
                print(f"- {tool.name}: {tool.description}")
            
            # Call the forecast tool for a location
            print("\nGetting weather forecast for New York City:")
            forecast = await session.call_tool(
                "get_forecast", 
                arguments={
                    "latitude": 40.7128, 
                    "longitude": -74.0060
                }
            )
            print(f"Forecast result:\n{forecast.result}")
            
            # Call the alerts tool for a state
            print("\nGetting weather alerts for California:")
            alerts = await session.call_tool(
                "get_alerts",
                arguments={"state": "CA"}
            )
            print(f"Alerts result:\n{alerts.result}")

if __name__ == "__main__":
    asyncio.run(main())
