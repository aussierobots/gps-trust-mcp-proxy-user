#!/usr/bin/env python3
"""GPS Trust MCP Proxy Server.

Bridges the remote GPS Trust MCP server at https://gt.aussierobots.com.au/mcp
to stdio transport for Claude Desktop and Claude Code.

The proxy injects the x-api-key header for authentication with the remote server.
API key can be provided via:
  1. Command-line argument: --api-key YOUR_KEY
  2. Environment variable: GPSTRUST_API_KEY
"""

import argparse
import os
import sys
from typing import NoReturn

from fastmcp import FastMCP
from fastmcp.server.proxy import ProxyClient


# GPS Trust MCP server URL
GPS_TRUST_MCP_URL = "https://gt.aussierobots.com.au/mcp"

# Environment variable name for API key
API_KEY_ENV_VAR = "GPSTRUST_API_KEY"


def get_api_key() -> str:
    """Get API key from command-line arguments or environment variable.

    Priority:
      1. --api-key command-line argument
      2. GPSTRUST_API_KEY environment variable

    Returns:
        str: The API key to use for authentication

    Raises:
        SystemExit: If no API key is provided
    """
    parser = argparse.ArgumentParser(
        description="GPS Trust MCP Proxy - Bridges HTTP MCP server to stdio transport",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Authentication:
  Provide API key via --api-key argument or {API_KEY_ENV_VAR} environment variable.

Example:
  # Using environment variable
  export {API_KEY_ENV_VAR}=your-api-key-here
  gt-mcp-proxy

  # Using command-line argument
  gt-mcp-proxy --api-key your-api-key-here
        """
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help=f"GPS Trust API key (overrides {API_KEY_ENV_VAR} env var)"
    )

    args = parser.parse_args()

    # Priority: CLI argument > environment variable
    api_key = args.api_key or os.environ.get(API_KEY_ENV_VAR)

    if not api_key:
        print(
            f"Error: No API key provided.\n"
            f"Provide via --api-key argument or {API_KEY_ENV_VAR} environment variable.\n",
            file=sys.stderr
        )
        sys.exit(1)

    return api_key


def create_proxy_config(api_key: str) -> dict:
    """Create FastMCP proxy configuration with authentication headers.

    Args:
        api_key: The GPS Trust API key

    Returns:
        Configuration dictionary for ProxyClient
    """
    return {
        "mcpServers": {
            "gps_trust": {
                "transport": "http",
                "url": GPS_TRUST_MCP_URL,
                "headers": {
                    "x-api-key": api_key
                }
            }
        }
    }


def main() -> NoReturn:
    """Main entry point for the GPS Trust MCP proxy server.

    This function:
      1. Gets the API key from CLI args or environment
      2. Creates a ProxyClient configured with the remote server URL and authentication
      3. Creates a FastMCP proxy using as_proxy()
      4. Runs the proxy on stdio transport (for Claude Desktop/Code)

    The proxy automatically forwards all tools, resources, and advanced MCP features
    (sampling, logging, progress notifications) from the remote GPS Trust server.
    """
    # Get API key
    api_key = get_api_key()

    # Create proxy configuration
    config = create_proxy_config(api_key)

    # Create proxy using FastMCP.as_proxy()
    # This uses the "fresh session" strategy - each request gets its own backend session
    # which is the recommended approach for concurrent safety
    proxy = FastMCP.as_proxy(
        ProxyClient(config),
        name="GPS Trust MCP Proxy"
    )

    # Run proxy on stdio transport (default)
    # This allows Claude Desktop and Claude Code to connect via stdin/stdout
    proxy.run()


if __name__ == "__main__":
    main()
