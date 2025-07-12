
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class MCPRequest(BaseModel):
    tool: str
    inputs: Dict

@app.post("/invoke")
def invoke(request: MCPRequest):
    # Mock logic: just echo input for demo
    if request.tool == "currency_converter":
        amount = request.inputs.get("amount", 0)
        from_currency = request.inputs.get("from_currency", "USD")
        to_currency = request.inputs.get("to_currency", "EUR")
        # Fake conversion rate
        rate = 0.9 if from_currency == "USD" and to_currency == "EUR" else 1.1
        return {
            "tool": request.tool,
            "result": {
                "converted_amount": round(amount * rate, 2),
                "currency": to_currency
            }
        }
    if request.tool == "summarize_text":
        text = request.inputs.get("text", "")
        return {
            "tool": request.tool,
            "result": {"summary": text[:50] + ("..." if len(text) > 50 else "")}
        }
    return {"tool": request.tool, "result": {"message": "Tool not implemented in mock backend"}}
