
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()
MCP_SERVER_URL = "http://127.0.0.1:8000/invoke"  # MCP backend URL

@app.post("/currency_converter")
def currency_converter(amount: float, from_currency: str, to_currency: str):
    payload = {
        "tool": "currency_converter",
        "inputs": {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency
        }
    }
    response = requests.post(MCP_SERVER_URL, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()["result"]

@app.post("/summarize_text")
def summarize_text(text: str):
    payload = {
        "tool": "summarize_text",
        "inputs": {"text": text}
    }
    response = requests.post(MCP_SERVER_URL, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()["result"]
