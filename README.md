
# MCP Proxy Implementation Examples

This repository demonstrates two approaches to bridging HTTP APIs with Model Context Protocol (MCP) servers:

1. **Production Approach**: Using FastMCP library (`proxy_server.py`)
2. **Educational Approach**: Manual implementation (`manual_proxy.py`)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the MCP Backend Server

```bash
python mcp_backend_server.py
```

This starts a real MCP server on port 8001 with three tools:
- `currency_converter`: Converts between currencies
- `summarize_text`: Summarizes text content
- `calculate`: Evaluates mathematical expressions

### 3. Choose Your Proxy Approach

#### Option A: Production FastMCP Proxy (Recommended)

```bash
python proxy_server.py
```

This starts a FastMCP-based proxy on port 8080 that properly handles MCP sessions.

#### Option B: Educational Manual Proxy

```bash
uvicorn manual_proxy:app --host 127.0.0.1 --port 9000
```

This starts a manual FastAPI implementation on port 9000 that demonstrates MCP protocol concepts but has session management limitations.

## Testing the Implementations

### Test the FastMCP Proxy (Production)

The FastMCP proxy exposes the full MCP protocol at `/mcp/`:

```bash
# Initialize MCP session
curl -X POST http://127.0.0.1:8080/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "id": "init",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "test-client", "version": "1.0"}
    }
  }'
```

For tool calls, you would need proper MCP session management. See `test_mcp_proxy.py` for examples.

### Test the Manual Proxy (Educational)

The manual proxy exposes simplified HTTP endpoints:

```bash
# Check health
curl http://127.0.0.1:9000/health

# Try currency conversion (will show educational error)
curl -X POST http://127.0.0.1:9000/currency_converter \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "from_currency": "USD", "to_currency": "EUR"}'
```

The manual proxy demonstrates the MCP protocol structure but has limitations with session management, providing educational error messages that point to the correct solution.

### Run the Test Script

```bash
python test_mcp_proxy.py
```

This script demonstrates proper MCP protocol usage with both the backend and proxy.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HTTP Client   │───▶│   Proxy Server  │───▶│  MCP Backend    │
│                 │    │                 │    │   Server        │
│ (curl, browser, │    │ • FastMCP       │    │                 │
│  mobile app)    │    │ • Manual Impl   │    │ • FastMCP       │
└─────────────────┘    └─────────────────┘    │ • 3 Tools       │
                                              └─────────────────┘
```

### Components

- **`mcp_backend_server.py`**: Real MCP server using FastMCP framework
- **`proxy_server.py`**: Production-ready proxy using FastMCP's ProxyClient
- **`manual_proxy.py`**: Educational manual implementation showing MCP protocol concepts
- **`test_mcp_proxy.py`**: Test script demonstrating proper MCP protocol usage

## Key Differences

| Aspect | FastMCP Proxy | Manual Proxy |
|--------|---------------|--------------|
| **Purpose** | Production use | Educational/Learning |
| **Session Management** | ✅ Full support | ❌ Limited (educational errors) |
| **MCP Compliance** | ✅ Complete | ⚠️ Partial (protocol demo) |
| **Endpoints** | `/mcp/` (full protocol) | Individual tool endpoints |
| **Error Handling** | Robust | Educational messages |
| **Performance** | Optimized | Basic |

## Educational Value

The manual proxy demonstrates:
- MCP JSON-RPC protocol structure
- Session initialization attempts
- Server-Sent Events (SSE) parsing
- Error handling patterns
- Why proper MCP client libraries are needed

When you test the manual proxy, it shows realistic error messages that explain the limitations and point to the production solution.

## Step-by-Step Testing Guide

### 1. Start All Servers

```bash
# Terminal 1: Start MCP backend
python mcp_backend_server.py

# Terminal 2: Start FastMCP proxy  
python proxy_server.py

# Terminal 3: Start manual proxy
uvicorn manual_proxy:app --host 127.0.0.1 --port 9000

# Terminal 4: Run tests
python test_mcp_proxy.py
```

### 2. Test Individual Components

**Test MCP Backend Health:**
```bash
curl -X POST http://127.0.0.1:8001/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "method": "initialize", "id": "init", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}'
```

**Test FastMCP Proxy:**
```bash
curl -X POST http://127.0.0.1:8080/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "method": "initialize", "id": "init", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}'
```

**Test Manual Proxy:**
```bash
# Health check
curl http://127.0.0.1:9000/health

# Educational tool call (shows limitation)
curl -X POST http://127.0.0.1:9000/currency_converter \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "from_currency": "USD", "to_currency": "EUR"}'
```

## Running Ports Summary

- **Port 8001**: MCP Backend Server
- **Port 8080**: FastMCP Proxy (Production)
- **Port 9000**: Manual Proxy (Educational)

## Files Overview

- `mcp_backend_server.py` - Real MCP backend with three tools
- `proxy_server.py` - Production FastMCP proxy implementation
- `manual_proxy.py` - Educational manual proxy implementation
- `test_mcp_proxy.py` - Test script showing proper MCP protocol usage
- `requirements.txt` - Python dependencies

## Key Learnings

1. **MCP requires session management**: The protocol is stateful, not stateless like REST
2. **FastMCP simplifies complexity**: Use proven libraries for production
3. **Manual implementation has value**: Understanding the protocol helps with debugging
4. **Proper error handling matters**: Educational errors help developers learn

## References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://gofastmcp.com/)
- [FastMCP Proxy Guide](https://gofastmcp.com/servers/proxy)
