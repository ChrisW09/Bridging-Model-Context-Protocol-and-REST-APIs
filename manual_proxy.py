"""
Manual MCP Proxy Implementation
This file demonstrates how to manually bridge HTTP requests to MCP (Model Context Protocol) calls.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI(
    title="Manual MCP Proxy",
    description="Manual FastAPI implementation showing how to bridge HTTP to MCP",
    version="1.0.0"
)

# Our MCP backend server URL
MCP_SERVER_URL = "http://127.0.0.1:8001/mcp/"

# Request models for better API documentation
class CurrencyRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str

class TextRequest(BaseModel):
    text: str

class CalculateRequest(BaseModel):
    expression: str

"""
Manual MCP Proxy Implementation
=====================================

This file demonstrates how to manually bridge HTTP requests to MCP (Model Context Protocol) calls.

EDUCATIONAL PURPOSE: This implementation shows the basic structure of how to communicate with
an MCP server, but it has limitations due to the session-based nature of the MCP protocol.

LIMITATION: MCP requires persistent sessions. This simple implementation doesn't handle session
persistence correctly. For production use, you should use a proper MCP client library like FastMCP.

For a production-ready solution, see proxy_server.py which uses FastMCP's ProxyClient.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI(
    title="Manual MCP Proxy (Educational)",
    description="Manual FastAPI implementation showing how to bridge HTTP to MCP (with limitations)",
    version="1.0.0"
)

# Our MCP backend server URL
MCP_SERVER_URL = "http://127.0.0.1:8001/mcp/"

# Request models for better API documentation
class CurrencyRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str

class TextRequest(BaseModel):
    text: str

class CalculateRequest(BaseModel):
    expression: str

def call_mcp_tool(tool_name: str, arguments: dict):
    """
    Helper function to call an MCP tool using proper JSON-RPC protocol.
    
    EDUCATIONAL NOTE: This implementation demonstrates the MCP protocol structure
    but has limitations with session management. In a real application, you would
    use a proper MCP client library that handles persistent sessions correctly.
    
    The FastMCP library (proxy_server.py) solves these session management issues.
    """
    
    # Use requests.Session to maintain connection/cookies (limited approach)
    session = requests.Session()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    
    # Step 1: Initialize MCP session 
    init_payload = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "id": "init",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "manual-proxy",
                "version": "1.0"
            }
        }
    }
    
    try:
        logger.info(f"Initializing MCP session for tool: {tool_name}")
        init_response = session.post(MCP_SERVER_URL, headers=headers, json=init_payload, timeout=10)
        logger.info(f"Init response status: {init_response.status_code}")
        
        if init_response.status_code != 200:
            logger.error(f"MCP initialization failed: {init_response.status_code}")
            raise HTTPException(status_code=503, detail="Failed to initialize MCP session")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"MCP backend not available: {e}")
        raise HTTPException(status_code=503, detail=f"MCP backend not available: {str(e)}")
    
    # Step 2: Call the tool using the same session
    # NOTE: This approach has limitations - MCP sessions are more complex than HTTP sessions
    tool_payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": f"call-{tool_name}",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    try:
        logger.info(f"Calling MCP tool: {tool_name} with args: {arguments}")
        tool_response = session.post(MCP_SERVER_URL, headers=headers, json=tool_payload, timeout=10)
        logger.info(f"Tool response status: {tool_response.status_code}")
        
        if tool_response.status_code != 200:
            error_msg = f"MCP tool call failed: {tool_response.text}"
            logger.error(error_msg)
            # Return a helpful error message for educational purposes
            if "Missing session ID" in tool_response.text:
                raise HTTPException(
                    status_code=503, 
                    detail={
                        "error": "Session management limitation",
                        "message": "This manual implementation has limitations with MCP session handling. Use FastMCP proxy (port 8080) for production.",
                        "fastmcp_alternative": "curl -X POST http://127.0.0.1:8080/mcp/ with proper MCP protocol",
                        "raw_error": tool_response.text
                    }
                )
            raise HTTPException(status_code=tool_response.status_code, detail=error_msg)
    except requests.exceptions.RequestException as e:
        logger.error(f"MCP backend error: {e}")
        raise HTTPException(status_code=503, detail=f"MCP backend error: {str(e)}")
    finally:
        session.close()
    
    # Parse the MCP response (which might be in SSE format)
    response_text = tool_response.text
    
    if "event: message" in response_text:
        # Extract JSON from SSE format
        lines = response_text.strip().split('\n')
        for line in lines:
            if line.startswith('data: '):
                try:
                    data = json.loads(line[6:])  # Remove 'data: ' prefix
                    if 'result' in data:
                        # Extract the actual tool result from MCP response
                        if 'content' in data['result']:
                            # MCP returns content array, get the text content
                            content = data['result']['content'][0]['text']
                            try:
                                return json.loads(content)  # Parse the tool's JSON result
                            except json.JSONDecodeError:
                                # Return as plain text if not JSON
                                return {"result": content, "type": "text"}
                        else:
                            return data['result']
                    elif 'error' in data:
                        logger.error(f"MCP tool error: {data['error']}")
                        raise HTTPException(status_code=400, detail=data['error'])
                except json.JSONDecodeError:
                    continue
    
    # Fallback for direct JSON response
    try:
        data = tool_response.json()
        if 'result' in data:
            return data['result']
        elif 'error' in data:
            logger.error(f"MCP response error: {data['error']}")
            raise HTTPException(status_code=400, detail=data['error'])
    except json.JSONDecodeError:
        pass
    
    logger.error(f"Unexpected MCP response format: {response_text}")
    raise HTTPException(status_code=500, detail="Unexpected MCP response format")

@app.get("/")
def root():
    """Root endpoint showing available endpoints."""
    return {
        "message": "Manual MCP Proxy is running",
        "endpoints": {
            "health": "GET /health",
            "currency_converter": "POST /currency_converter",
            "summarize_text": "POST /summarize_text",
            "calculate": "POST /calculate"
        }
    }

@app.post("/currency_converter")
def currency_converter(request: CurrencyRequest):
    """Convert currency using the MCP backend."""
    logger.info(f"Currency conversion request: {request}")
    try:
        result = call_mcp_tool("currency_converter", {
            "amount": request.amount,
            "from_currency": request.from_currency,
            "to_currency": request.to_currency
        })
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Internal error in currency_converter: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.post("/summarize_text")
def summarize_text(request: TextRequest):
    """Summarize text using the MCP backend."""
    logger.info(f"Text summarization request: {len(request.text)} characters")
    try:
        result = call_mcp_tool("summarize_text", {
            "text": request.text
        })
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Internal error in summarize_text: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.post("/calculate")
def calculate(request: CalculateRequest):
    """Calculate a mathematical expression using the MCP backend."""
    logger.info(f"Calculation request: {request.expression}")
    try:
        result = call_mcp_tool("calculate", {
            "expression": request.expression
        })
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Internal error in calculate: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/health")
def health_check():
    """Check if the manual proxy and MCP backend are working."""
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        init_payload = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "id": "health-check",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "health-check", "version": "1.0"}
            }
        }
        response = requests.post(MCP_SERVER_URL, headers=headers, json=init_payload, timeout=5)
        
        return {
            "status": "healthy" if response.status_code == 200 else "degraded",
            "mcp_backend": "connected" if response.status_code == 200 else "disconnected",
            "backend_url": MCP_SERVER_URL,
            "proxy_type": "manual_fastapi"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "mcp_backend": "disconnected",
            "backend_url": MCP_SERVER_URL,
            "proxy_type": "manual_fastapi",
            "error": str(e)
        }

# For running with uvicorn manually
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Manual MCP Proxy server...")
    uvicorn.run(app, host="127.0.0.1", port=9000, log_level="info")
