#!/usr/bin/env python3
"""
Real MCP backend server using FastMCP framework.
This implements proper MCP tools that can be proxied.
"""

from fastmcp import FastMCP
from typing import Dict, Any

# Create the MCP server
server = FastMCP("MCP-Backend")

@server.tool()
def currency_converter(amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
    """Convert currency from one type to another with mock exchange rates."""
    # Mock conversion rates for demo purposes
    rates = {
        ("USD", "EUR"): 0.9,
        ("EUR", "USD"): 1.1,
        ("USD", "GBP"): 0.8,
        ("GBP", "USD"): 1.25,
        ("EUR", "GBP"): 0.85,
        ("GBP", "EUR"): 1.18,
    }
    
    # Get the conversion rate or default to 1.0
    rate = rates.get((from_currency, to_currency), 1.0)
    converted_amount = round(amount * rate, 2)
    
    return {
        "converted_amount": converted_amount,
        "currency": to_currency,
        "original_amount": amount,
        "original_currency": from_currency,
        "exchange_rate": rate
    }

@server.tool()
def summarize_text(text: str) -> Dict[str, str]:
    """Summarize the given text by truncating it."""
    # Simple text summarization by truncating
    max_length = 50
    summary = text[:max_length] + ("..." if len(text) > max_length else "")
    
    return {
        "summary": summary,
        "original_length": len(text),
        "summary_length": len(summary)
    }

@server.tool()
def calculate(expression: str) -> Dict[str, Any]:
    """Safely evaluate a mathematical expression."""
    try:
        # Only allow basic mathematical operations for safety
        allowed_chars = set('0123456789+-*/()., ')
        if not all(c in allowed_chars for c in expression):
            return {"error": "Invalid characters in expression"}
        
        result = eval(expression)
        return {
            "expression": expression,
            "result": result
        }
    except Exception as e:
        return {
            "expression": expression,
            "error": str(e)
        }

if __name__ == "__main__":
    # Run the MCP server on stdio (for Claude Desktop integration)
    # You can also run it on HTTP for testing: server.run(transport="http", port=8001)
    server.run(transport="http", host="127.0.0.1", port=8001)
