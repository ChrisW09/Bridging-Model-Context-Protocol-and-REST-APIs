
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

### 3. Start (or mock) your MCP backend server

You can use your own MCP server or mock one using FastAPI for testing:

```bash
uvicorn mock_mcp_backend:app --reload --port 8000
```

### 4. Run the FastMCP proxy

```bash
python proxy_server.py
```
- This exposes all MCP tools over HTTP at `http://localhost:8080/mcp`.

### 5. Run the manual FastAPI adapter (optional)

```bash
uvicorn manual_proxy:app --reload --port 9000
```
- This exposes `/currency_converter` and `/summarize_text` for demo at `http://localhost:9000/`.

---

## 🧩 Example HTTP Requests

**With FastMCP Proxy:**

```bash
curl -X POST http://localhost:8080/mcp   -H "Content-Type: application/json"   -d '{"tool": "currency_converter", "inputs": {"amount": 100, "from_currency": "USD", "to_currency": "EUR"}}'
```

**With Manual Adapter:**

```bash
curl -X POST "http://localhost:9000/currency_converter?amount=100&from_currency=USD&to_currency=EUR"
```

---

## 📁 File Structure

```
.
├── proxy_server.py        # FastMCP proxy server example
├── manual_proxy.py        # Manual FastAPI adapter example
├── mock_mcp_backend.py    # (Optional) Mock MCP backend for local testing
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📝 Details

### proxy_server.py

Uses FastMCP's `as_proxy` to automatically expose all backend tools over a single HTTP endpoint. Great for production, auto-discovery, and minimizing boilerplate.

### manual_proxy.py

A FastAPI example showing how to manually bridge specific HTTP endpoints to your MCP backend. Great for custom logic, demos, or when only a few tools are needed.

### mock_mcp_backend.py (for local testing)

Run this script to start a dummy MCP backend on `localhost:8000`.

---

## 📝 License

MIT
