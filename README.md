# MCP Proxy Implementation: Bridging HTTP and Model Context Protocol

This repository demonstrates comprehensive approaches to bridging HTTP APIs with the Model Context Protocol (MCP), providing both production-ready solutions and educational examples for understanding MCP integration patterns.

## 🎯 Overview

The Model Context Protocol (MCP) is a standardized protocol for AI applications to securely connect to external data sources and tools. This repository showcases two distinct approaches to creating HTTP-to-MCP bridges:

### 1. **Production Approach** (`proxy_server.py`)
- Uses the FastMCP library with `ProxyClient`
- Full MCP protocol compliance with session management
- Streamable HTTP transport for optimal performance
- Production-ready with proper error handling

### 2. **Educational Approach** (`manual_proxy.py`)
- Manual FastAPI implementation showing MCP protocol internals
- Demonstrates JSON-RPC structure and session concepts
- Includes detailed comments explaining limitations
- Perfect for learning MCP protocol fundamentals

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/JSON-RPC    ┌─────────────────┐    MCP Protocol    ┌─────────────────┐
│   HTTP Client   │ ──────────────────► │   MCP Proxy     │ ─────────────────► │  MCP Backend    │
│  (curl, app)    │                     │ (FastMCP/Manual)│                    │    Server       │
└─────────────────┘                     └─────────────────┘                    └─────────────────┘
                                                │                                         │
                                                │                                         │
                                        Session Management                        Tool Implementations:
                                        Protocol Translation                      - currency_converter
                                        Error Handling                           - summarize_text
                                                                                - calculate
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd Bridging-Model-Context-Protocol-and-REST-APIs

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the MCP Backend Server

```bash
python mcp_backend_server.py
```

**Server Details:**
- **Port:** 8001
- **Endpoint:** `http://127.0.0.1:8001/mcp/`
- **Protocol:** MCP JSON-RPC over HTTP with SSE responses
- **Tools Available:**
  - `currency_converter`: Convert between currencies with real-time rates
  - `summarize_text`: AI-powered text summarization
  - `calculate`: Mathematical expression evaluation

### 3. Choose Your Proxy Implementation

#### Option A: Production FastMCP Proxy (⭐ Recommended)

```bash
python proxy_server.py
```

**Features:**
- **Port:** 8080
- **Full MCP compliance:** Complete protocol support
- **Session management:** Automatic session handling and cleanup
- **Error handling:** Robust error propagation and recovery
- **Performance:** Optimized for production workloads

#### Option B: Educational Manual Proxy

```bash
uvicorn manual_proxy:app --host 127.0.0.1 --port 9000
```

**Features:**
- **Port:** 9000
- **Educational focus:** Detailed comments and explanations
- **Protocol demonstration:** Shows MCP JSON-RPC structure
- **Limitations highlighted:** Clear documentation of constraints
- **FastAPI integration:** RESTful endpoint patterns

## 🧪 Testing and Validation

### Comprehensive Test Suite

Run the included test script to verify all components:

```bash
python test_mcp_proxy.py
```

**Test Coverage:**
- ✅ MCP backend server connectivity
- ✅ Proxy initialization and session management
- ✅ JSON-RPC protocol compliance
- ✅ Error handling and recovery
- ✅ Response format validation

### Manual Testing

#### Test the FastMCP Proxy (Recommended)

```bash
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

Call a tool through the proxy:
```bash
curl -X POST http://127.0.0.1:8080/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "id": "call-1",
    "params": {
      "name": "currency_converter",
      "arguments": {
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "EUR"
      }
    }
  }'
```

#### Test the Educational Manual Proxy

Check proxy health:
```bash
curl http://127.0.0.1:9000/health
```

Test currency conversion:
```bash
curl -X POST http://127.0.0.1:9000/currency_converter \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100,
    "from_currency": "USD", 
    "to_currency": "EUR"
  }'
```

Test text summarization:
```bash
curl -X POST http://127.0.0.1:9000/summarize_text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The Model Context Protocol (MCP) is an open standard that enables AI applications to securely connect to external data sources and tools. It provides a universal way for AI systems to access databases, APIs, file systems, and other resources while maintaining security and user control."
  }'
```

Test mathematical calculations:
```bash
curl -X POST http://127.0.0.1:9000/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "2 + 2 * 3"
  }'
```

## 📋 Detailed Component Documentation

### MCP Backend Server (`mcp_backend_server.py`)

A production-ready MCP server implementation that provides three essential tools:

#### 🔧 Available Tools

| Tool | Purpose | Parameters | Example Response |
|------|---------|------------|------------------|
| **currency_converter** | Convert between currencies | `amount`, `from_currency`, `to_currency` | `{"converted_amount": 85.0, "currency": "EUR", "exchange_rate": 0.85}` |
| **summarize_text** | Summarize long text content | `text` | `{"summary": "Brief summary of the text", "length": 25}` |
| **calculate** | Evaluate mathematical expressions | `expression` | `{"result": 8, "expression": "2 + 2 * 3"}` |

#### 🔌 Protocol Implementation

- **JSON-RPC 2.0** compliance
- **Server-Sent Events (SSE)** for real-time responses
- **Session management** with proper initialization
- **Error handling** with detailed error messages
- **Resource management** with automatic cleanup

### FastMCP Proxy Server (`proxy_server.py`)

A minimal yet powerful proxy implementation using the FastMCP library:

```python
from fastmcp import FastMCP
from fastmcp.server.proxy import ProxyClient

# Create a proxy with full MCP feature support
proxy = FastMCP.as_proxy(
    ProxyClient("http://127.0.0.1:8001/mcp/"),
    name="HTTPProxy"
)

# Run with streamable-http transport
proxy.run(transport="streamable-http", host="127.0.0.1", port=8080)
```

#### ✨ Key Features

- **Complete MCP Protocol Support**: All MCP features are automatically forwarded
- **Session Isolation**: Each client gets independent session management
- **Automatic Error Handling**: Robust error propagation and recovery
- **Performance Optimized**: Streamable HTTP transport for efficiency
- **Zero Configuration**: Works out-of-the-box with any MCP server

### Manual Proxy Server (`manual_proxy.py`)

An educational implementation that demonstrates MCP protocol internals:

#### 🎓 Educational Value

- **Protocol Demonstration**: Shows JSON-RPC structure and flow
- **Session Management**: Illustrates the challenges of MCP sessions
- **Error Handling**: Examples of proper error propagation
- **REST API Patterns**: FastAPI integration for familiar HTTP endpoints

#### ⚠️ Known Limitations

- **Session Persistence**: Simplified session handling (not production-ready)
- **Connection Pooling**: Basic request handling without optimization
- **Error Recovery**: Limited error recovery mechanisms
- **Feature Coverage**: Doesn't support all MCP advanced features

## 🏛️ MCP Protocol Deep Dive

### Understanding JSON-RPC 2.0 Over HTTP

The Model Context Protocol uses JSON-RPC 2.0 as its base communication protocol:

#### Request Structure
```json
{
  "jsonrpc": "2.0",
  "method": "method_name",
  "id": "unique_identifier",
  "params": {
    "parameter1": "value1",
    "parameter2": "value2"
  }
}
```

#### Response Structure
```json
{
  "jsonrpc": "2.0",
  "id": "unique_identifier",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Tool execution result"
      }
    ]
  }
}
```

### Session Lifecycle

1. **Initialization**: Client sends `initialize` method with capabilities
2. **Tool Discovery**: Client can call `tools/list` to discover available tools
3. **Tool Execution**: Client calls `tools/call` with specific tool and arguments
4. **Session Management**: Server maintains state throughout the session
5. **Cleanup**: Automatic cleanup when connection is closed

### Error Handling Patterns

MCP defines standard error codes and structures:

```json
{
  "jsonrpc": "2.0",
  "id": "call-id",
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "details": "Specific error information"
    }
  }
}
```

## 🔧 Configuration and Customization

### Environment Variables

Set these environment variables to customize behavior:

```bash
# MCP Backend Configuration
export MCP_BACKEND_HOST=127.0.0.1
export MCP_BACKEND_PORT=8001

# Proxy Configuration  
export PROXY_HOST=127.0.0.1
export FASTMCP_PROXY_PORT=8080
export MANUAL_PROXY_PORT=9000

# Logging
export LOG_LEVEL=INFO
export MCP_DEBUG=false
```

### Custom Tool Implementation

To add new tools to the MCP backend:

```python
@mcp_server.tool()
def your_custom_tool(parameter1: str, parameter2: int) -> str:
    """
    Your custom tool description.
    
    Args:
        parameter1: Description of first parameter
        parameter2: Description of second parameter
        
    Returns:
        Tool execution result
    """
    # Your implementation here
    result = f"Processed {parameter1} with value {parameter2}"
    return result
```

### Proxy Customization

Extend the manual proxy with additional endpoints:

```python
@app.post("/your_endpoint")
def your_endpoint(request: YourRequestModel):
    """Custom endpoint that calls MCP backend."""
    try:
        result = call_mcp_tool("your_custom_tool", {
            "parameter1": request.param1,
            "parameter2": request.param2
        })
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. **Connection Refused Errors**

**Problem**: `requests.exceptions.ConnectionError: Connection refused`

**Solutions**:
- Verify MCP backend server is running: `python mcp_backend_server.py`
- Check port availability: `lsof -i :8001`
- Verify correct URL in proxy configuration

#### 2. **Session Management Issues**

**Problem**: "Missing session ID" or session-related errors

**Solutions**:
- Use FastMCP proxy for production (handles sessions automatically)
- For manual proxy, ensure proper session initialization
- Check that `initialize` method is called before tool calls

#### 3. **JSON-RPC Format Errors**

**Problem**: Invalid JSON-RPC format or structure

**Solutions**:
- Verify JSON-RPC 2.0 compliance (`jsonrpc`, `method`, `id` fields)
- Check parameter structure matches expected format
- Use test script to verify correct protocol usage

#### 4. **Tool Not Found Errors**

**Problem**: Tool name not recognized by MCP backend

**Solutions**:
- List available tools: Use `tools/list` method
- Verify tool name spelling and case sensitivity
- Check that MCP backend has registered the tool

#### 5. **Performance Issues**

**Problem**: Slow response times or connection timeouts

**Solutions**:
- Use FastMCP proxy instead of manual implementation
- Increase timeout values in requests
- Check network connectivity and latency
- Monitor server resource usage

### Debug Mode

Enable detailed logging for troubleshooting:

```bash
# Set environment variable
export MCP_DEBUG=true

# Or modify Python logging level
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Health Check Endpoints

Monitor system health using built-in endpoints:

```bash
# FastMCP Proxy (via MCP protocol)
curl -X POST http://127.0.0.1:8080/mcp/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "ping", "id": "health"}'

# Manual Proxy  
curl http://127.0.0.1:9000/health

# MCP Backend (direct)
curl -X POST http://127.0.0.1:8001/mcp/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "initialize", "id": "health", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "health", "version": "1.0"}}}'
```

## 📚 Additional Resources

### MCP Protocol Documentation
- **Official Specification**: [Model Context Protocol](https://spec.modelcontextprotocol.io/)
- **FastMCP Library**: [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- **Protocol Specification**: [MCP JSON-RPC Specification](https://spec.modelcontextprotocol.io/specification/basic/transports/)

### Development Resources
- **FastAPI Documentation**: [FastAPI Docs](https://fastapi.tiangolo.com/)
- **JSON-RPC 2.0 Specification**: [JSON-RPC 2.0](https://www.jsonrpc.org/specification)
- **Python MCP Examples**: [MCP Python Examples](https://github.com/modelcontextprotocol/python-sdk)

### Community and Support
- **MCP GitHub**: [Official Repository](https://github.com/modelcontextprotocol)
- **Discord Community**: [MCP Discord](https://discord.gg/modelcontextprotocol)
- **Issue Tracking**: Use GitHub issues for bug reports and feature requests

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Install development dependencies**: `pip install -r requirements-dev.txt`
4. **Run tests**: `python -m pytest tests/`
5. **Submit a pull request**

### Code Standards

- **PEP 8** compliance for Python code
- **Type hints** for function signatures
- **Docstrings** for all public functions and classes
- **Error handling** with appropriate exception types
- **Testing** for new functionality

### Areas for Contribution

- **Additional Tools**: Implement new MCP tools
- **Performance Optimization**: Improve proxy performance
- **Documentation**: Enhance guides and examples
- **Testing**: Expand test coverage
- **Examples**: Create integration examples

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastMCP Team**: For the excellent MCP library and tooling
- **Model Context Protocol**: For defining the standard
- **FastAPI Community**: For the robust web framework
- **Python Community**: For the extensive ecosystem

---

**Happy coding with MCP! 🚀**

For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/your-repo/mcp-proxy-examples).

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
