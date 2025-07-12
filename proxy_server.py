
from fastmcp import FastMCP
from fastmcp.server.proxy import ProxyClient

# Create a proxy with full MCP feature support using ProxyClient
# Connect to the proper MCP backend server (not the simple HTTP mock)
proxy = FastMCP.as_proxy(
    ProxyClient("http://127.0.0.1:8001/mcp/"),
    name="HTTPProxy"
)

if __name__ == "__main__":
    # Run the proxy via streamable-http transport for better session handling
    proxy.run(transport="streamable-http", host="127.0.0.1", port=8080)
