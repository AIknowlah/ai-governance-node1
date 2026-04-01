"""
GraphState TypedDict Definition

This defines the state schema used across all nodes in the LangGraph system.

Each node reads from and writes to this shared state object.

Author: Chandhiran
Date: April 1, 2026
"""

from typing import TypedDict, List


class GraphState(TypedDict):
    """
    State schema for the LangGraph multi-node system.
    
    This TypedDict defines all fields that can be passed between nodes.
    Each node should only read/write the fields it needs.
    
    Fields:
        request_id: Unique identifier for this request (UUID)
        user_input: Original user input (before sanitization)
        sanitized_input: User input after NRIC redaction and sanitization
        pdpa_flags: List of PDPA-related flags (e.g., "nric_found", "medical_data")
        ai_verify_principles: List of AI Verify principles applied (e.g., "P1_Transparency")
        error: Error message if something went wrong (empty string if no error)
    """
    
    # Node 1 fields (Input Sanitizer)
    request_id: str
    user_input: str
    sanitized_input: str
    pdpa_flags: List[str]
    ai_verify_principles: List[str]
    error: str
    
    # Node 2 fields (Query Router) - to be added when Node 2 is built
    # route: str  # "general", "report", "emergency"
    
    # Node 3 fields (Gemini Caller) - to be added when Node 3 is built
    # gemini_response: str
    
    # Node 4 fields (Output Labeler) - to be added when Node 4 is built
    # labeled_response: str
    
    # Node 5 fields (Rate Limiter) - to be added when Node 5 is built
    # request_count: int