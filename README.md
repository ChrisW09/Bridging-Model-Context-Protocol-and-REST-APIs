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

Starts a FastMCP-based proxy on port 8080 with full MCP protocol support.

#### Option B: Educational Manual Proxy

```bash
uvicorn manual_proxy:app --host 127.0.0.1 --port 9000
```

Starts a manual FastAPI implementation on port 9000 that demonstrates MCP protocol concepts.

## Testing

### Test the FastMCP Proxy

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

### Test the Manual Proxy

```bash
# Check health
curl http://127.0.0.1:9000/health

# Try currency conversion (shows educational limitation)
curl -X POST http://127.0.0.1:9000/currency_converter \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "from_currency": "USD", "to_currency": "EUR"}'
```

### Run Test Script

```bash
python test_mcp_proxy.py
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HTTP Client   │───▶│   Proxy Server  │───▶│  MCP Backend    │
│                 │    │                 │    │   Server        │
│ (curl, browser, │    │ • FastMCP       │    │                 │
│  mobile app)    │    │ • Manual Impl   │    │ • FastMCP       │
└─────────────────┘    └─────────────────┘    │ • 3 Tools       │
                                              └─────────────────┘
```

## Key Differences

| Aspect | FastMCP Proxy | Manual Proxy |
|--------|---------------|--------------|
| **Purpose** | Production use | Educational/Learning |
| **Session Management** | ✅ Full support | ❌ Limited (shows errors) |
| **MCP Compliance** | ✅ Complete | ⚠️ Partial (protocol demo) |
| **Endpoints** | `/mcp/` (full protocol) | Individual tool endpoints |
| **Error Handling** | Robust | Educational messages |

## Files

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

## Running All Components

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

## References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://gofastmcp.com/)
- [FastMCP Proxy Guide](https://gofastmcp.com/servers/proxy)
