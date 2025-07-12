
from fastmcp import FastMCP, Client

# URL to your MCP backend server
backend = Client("http://127.0.0.1:8000/invoke")

# Proxy exposes all backend tools/resources as HTTP endpoints
proxy = FastMCP.as_proxy(backend, name="HTTPProxy")

if __name__ == "__main__":
    proxy.run(transport="streamable-http", host="127.0.0.1", port=8080)
