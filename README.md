# GPS Trust MCP Proxy

Python proxy that connects Claude Desktop and Claude Code to the GPS Trust MCP server at `https://gt.aussierobots.com.au/mcp`.

## Quick Start

### 1. Clone this repository

```bash
git clone https://github.com/aussierobots/gps-trust-mcp-proxy-user.git
cd gps-trust-mcp-proxy-user
```

### 2. Install dependencies

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

This will:
- Create a virtual environment in `.venv/`
- Install FastMCP 2.12+ and dependencies
- Generate `uv.lock` file

### 3. Get your API key

Contact your GPS Trust administrator to obtain an API key.

### 4. Configure Claude Desktop

**macOS**: Edit `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: Edit `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration (replace the path and API key):

```json
{
  "mcpServers": {
    "gps-trust": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/gps-trust-mcp-proxy-user",
        "gt-mcp-proxy"
      ],
      "env": {
        "GPSTRUST_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**macOS Example**:
```json
{
  "mcpServers": {
    "gps-trust": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/yourname/gps-trust-mcp-proxy-user",
        "gt-mcp-proxy"
      ],
      "env": {
        "GPSTRUST_API_KEY": "your-actual-api-key"
      }
    }
  }
}
```

**Windows Example**:
```json
{
  "mcpServers": {
    "gps-trust": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "C:\\Users\\yourname\\gps-trust-mcp-proxy-user",
        "gt-mcp-proxy"
      ],
      "env": {
        "GPSTRUST_API_KEY": "your-actual-api-key"
      }
    }
  }
}
```

### 5. Restart Claude Desktop

After saving the configuration, restart Claude Desktop. The GPS Trust tools should appear in the tool palette.

## Alternative: Claude Code

Create or edit `.claude/config.json` in your project:

```json
{
  "mcpServers": {
    "gps-trust": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/gps-trust-mcp-proxy-user",
        "gt-mcp-proxy"
      ],
      "env": {
        "GPSTRUST_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Then run `/mcp reload` in Claude Code.

## Available Tools

Once connected, you'll have access to 23+ GPS Trust MCP tools:

- **Entity Info** (1 tool) - Discover your API key's entity type and capabilities
- **Device Reading** (5 tools) - Current device state (location, satellites, orbital, security, metadata)
- **Device History** (4 tools) - Historical location data, tracks, and accuracy trends
- **Entity Discovery** (7 tools) - Discover robots, stations, and devices in your account
- **GPS Trust Map** (3 tools) - Query GPS trust levels by location or geohash
- **Metadata** (2 tools) - Field and entity metadata lookups
- **Coordinate Conversion** (2 tools) - Convert between LLH and ECEF coordinate systems

## Testing

Test the proxy is working:

```bash
export GPSTRUST_API_KEY="your-api-key-here"
uv run gt-mcp-proxy
```

The proxy should start and wait for MCP protocol messages on stdin (press Ctrl+C to exit).

## Troubleshooting

### Tools don't appear in Claude Desktop

1. **Check the absolute path** in your configuration is correct
2. **Restart Claude Desktop** after making config changes
3. **View logs**: Help → View Logs in Claude Desktop menu

### "No API key provided" error

Make sure the `GPSTRUST_API_KEY` environment variable is set in the configuration file.

### Connection errors

Test the server is accessible:
```bash
curl -H "x-api-key: your-api-key" https://gt.aussierobots.com.au/mcp
```

If this fails, check:
- Your API key is valid
- You have internet connectivity
- The GPS Trust server is running

## How It Works

```
┌─────────────────┐
│ Claude Desktop  │
│ or Claude Code  │
└────────┬────────┘
         │ stdio
         ▼
┌─────────────────┐
│  GPS Trust MCP  │
│     Proxy       │
│  (This Repo)    │
└────────┬────────┘
         │ HTTP + x-api-key
         ▼
┌─────────────────┐
│  GPS Trust MCP  │
│     Server      │
│  (AWS Lambda)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    DynamoDB     │
│  (Device Data)  │
└─────────────────┘
```

The proxy:
1. Connects to Claude Desktop/Code via stdio transport
2. Forwards MCP requests to the remote GPS Trust server over HTTP
3. Injects your API key for authentication
4. Relays responses back to Claude

## Support

For issues or questions, contact your GPS Trust administrator.

## License

See [LICENSE](LICENSE)
