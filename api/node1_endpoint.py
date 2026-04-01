"""
Moonshot-Compatible API Endpoint for Node 1 (Input Sanitizer)

This wrapper makes Node 1 testable by Project Moonshot by exposing it as an HTTP endpoint.

Moonshot expects:
    POST /chat
    {
        "prompt": "user input here"
    }
    
    Response:
    {
        "response": "sanitized output here"
    }

Author: Chandhiran
Date: April 1, 2026
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nodes.node_1_input_sanitizer import input_sanitizer_node
from src.nodes.graph_state import GraphState

app = FastAPI(
    title="Node 1: NRIC Input Sanitizer",
    description="PDPA-compliant NRIC redaction endpoint for Moonshot testing",
    version="1.0.0"
)

class MoonshotRequest(BaseModel):
    """Moonshot's expected request format"""
    prompt: str
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 1000

class MoonshotResponse(BaseModel):
    """Moonshot's expected response format"""
    response: str
    metadata: Optional[dict] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    node: str

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "Node 1: NRIC Input Sanitizer",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat (POST)",
            "test": "/test (GET)"
        }
    }

@app.get("/health")
def health_check() -> HealthResponse:
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        node="node_1_input_sanitizer"
    )

@app.post("/chat")
def chat(request: MoonshotRequest) -> MoonshotResponse:
    """
    Main endpoint that Moonshot will call.
    
    This translates Moonshot's format into Node 1's GraphState format,
    processes it, and returns the sanitized output.
    """
    try:
        # Convert Moonshot request to GraphState
        state: GraphState = {
            "request_id": "",  # Will be auto-generated
            "user_input": request.prompt,
            "sanitized_input": "",
            "pdpa_flags": [],
            "ai_verify_principles": [],
            "error": ""
        }
        
        # Process through Node 1
        result = input_sanitizer_node(state)
        
        # Check for errors
        if result.get("error"):
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Convert back to Moonshot response format
        return MoonshotResponse(
            response=result["sanitized_input"],
            metadata={
                "pdpa_flags": result["pdpa_flags"],
                "ai_verify_principles": result["ai_verify_principles"],
                "nric_detected": "nric_found" in result["pdpa_flags"],
                "redacted": result["user_input"] != result["sanitized_input"]
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/test")
def test_endpoint():
    """
    Quick test endpoint to verify Node 1 is working.
    Tests with a sample NRIC.
    """
    test_input = "My NRIC is S1234567A and I need help"
    
    state: GraphState = {
        "request_id": "test-123",
        "user_input": test_input,
        "sanitized_input": "",
        "pdpa_flags": [],
        "ai_verify_principles": [],
        "error": ""
    }
    
    result = input_sanitizer_node(state)
    
    return {
        "test": "NRIC Redaction Test",
        "input": test_input,
        "output": result["sanitized_input"],
        "nric_detected": "nric_found" in result["pdpa_flags"],
        "flags": result["pdpa_flags"],
        "principles": result["ai_verify_principles"],
        "status": "✅ PASS" if result["sanitized_input"] == "My NRIC is S****567A and I need help" else "❌ FAIL"
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 Starting Node 1 API Endpoint for Moonshot Testing")
    print("="*60)
    print("\n📍 Endpoint: http://localhost:8001")
    print("\n🔍 Test it:")
    print("   - Health: http://localhost:8001/health")
    print("   - Quick test: http://localhost:8001/test")
    print("   - Chat (POST): http://localhost:8001/chat")
    print("\n💻 Connect to Moonshot:")
    print('   moonshot add_endpoint -n "node1" -u "http://localhost:8001/chat"')
    print("\n⏹️  Stop: Press Ctrl+C")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")