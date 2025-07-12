
# 🛰️ Exposing MCP Tools as Classic HTTP Endpoints

A reference implementation for bridging Model Context Protocol (MCP) with classic REST APIs, as described in [this Medium article](https://medium.com/@YOUR-ARTICLE-LINK).

This repo provides:
- A proxy server exposing MCP tools over HTTP with [FastMCP](https://github.com/jlowin/fastmcp)
- A manual FastAPI adapter for a handful of MCP tools
- Example requests and detailed explanation

---

## 🚦 What is MCP?

MCP (Model Context Protocol) is a protocol designed for **function-style, tool-centric AI and agent orchestration**—not just for reading/writing database resources. MCP calls often use HTTP as a transport but are organized around invoking tools and models, not resource URLs.

---

## 📊 Architecture

```
[ REST API Client ]
      |
      v
[ Proxy Server (FastMCP or FastAPI) ]
      |
      v
[ MCP Server ]
```

---

## ⚡ Quick Start

### 1. Clone this repo

```bash
git clone https://github.com/YOUR-USERNAME/mcp-http-proxy-example.git
cd mcp-http-proxy-example
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the MCP backend server

```bash
python mcp_backend_server.py
```
- Real MCP server built with FastMCP framework on port 8001
- Implements proper MCP tools: `currency_converter`, `summarize_text`, `calculate`
- Full MCP protocol support with JSON-RPC

### 4. Run the FastMCP proxy server

```bash
python proxy_server.py
```
- **Proper MCP Proxy**: Built with FastMCP's `ProxyClient` following [official documentation](https://gofastmcp.com/servers/proxy)
- **Full MCP Protocol**: Supports JSON-RPC 2.0 with session isolation and advanced MCP features
- **Session Management**: Each request gets isolated backend sessions for safe concurrency
- **Transport Bridging**: Connects to MCP backend on port 8001, exposes via HTTP on port 8080
- **Endpoint**: `http://127.0.0.1:8080/mcp/` (requires proper MCP client with JSON-RPC)

### 5. Test the implementation

```bash
python test_mcp_proxy.py
```

---

## 🧩 Example Usage

**Testing the FastMCP Proxy:**

```bash
python test_mcp_proxy.py
```

**Proper MCP JSON-RPC Protocol (for FastMCP Proxy):**

```bash
# Initialize session
curl -X POST http://127.0.0.1:8080/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "method": "initialize", "id": "init", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test-client", "version": "1.0"}}}'

# Call a tool (requires session management)
curl -X POST http://127.0.0.1:8080/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "method": "tools/call", "id": "call-1", "params": {"name": "currency_converter", "arguments": {"amount": 100, "from_currency": "USD", "to_currency": "EUR"}}}'
```

---

## 📁 File Structure

```
.
├── proxy_server.py        # FastMCP proxy server (proper MCP implementation)
├── mcp_backend_server.py  # Real MCP backend server with FastMCP
├── test_mcp_proxy.py      # Test script demonstrating MCP protocol
├── requirements.txt
└── README.md
```

---

## 📝 Details

### proxy_server.py

**Proper FastMCP Proxy Implementation** following the [official FastMCP documentation](https://gofastmcp.com/servers/proxy):
- Uses `ProxyClient` for automatic session isolation and full MCP feature support
- Implements transport bridging (connects to MCP backend, exposes via HTTP)
- Forwards advanced MCP features (sampling, elicitation, logging, progress)
- Safe concurrent request handling with isolated backend sessions
- Full JSON-RPC 2.0 MCP protocol compliance

### mcp_backend_server.py

**Real MCP Server** built with FastMCP framework:
- Implements proper MCP tools: `currency_converter`, `summarize_text`, `calculate`
- Full MCP protocol support with automatic tool discovery
- Can be used with any MCP client (Claude Desktop, custom clients, etc.)
- Demonstrates proper FastMCP server development patterns

### mock_mcp_backend.py (for local testing)

Run this script to start a dummy MCP backend on `localhost:8000`.

---

## 📝 License

MIT
