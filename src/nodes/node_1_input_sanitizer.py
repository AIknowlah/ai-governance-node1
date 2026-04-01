"""
Node 1: Input Sanitizer
PDPA Compliance Gateway - First line of defense

Governance Controls:
- PDPA Section 24: Purpose Limitation (redact unnecessary PII)
- PDPA Section 25: Consent (assume no consent to display NRICs)
- AI Verify P2: Safety (prevent identity exposure)
- AI Verify P9: Accountability (audit all inputs)
"""

import uuid
import time
from typing import TypedDict, List
from src.utils.nric_sanitizer import redact_nric, hash_pii, contains_prohibited_keywords
from src.utils.audit_logger import AuditLogger


# LangGraph State Schema
class GraphState(TypedDict):
    request_id: str              # UUID for audit trail
    user_input: str              # Raw input from user
    sanitized_input: str         # NRIC-redacted version
    pdpa_flags: List[str]        # e.g., ['nric_found', 'medical_data']
    ai_verify_principles: List[str]  # e.g., ['P2_Safety', 'P9_Accountability']
    error: str                   # Error message if node fails


def input_sanitizer_node(state: GraphState) -> GraphState:
    """
    Node 1: Sanitize user input before processing.
    
    Returns:
        Updated state with sanitized_input and compliance flags
    """
    start_time = time.time()
    logger = AuditLogger()
    
    # Generate request ID if not present
    if not state.get("request_id"):
        state["request_id"] = str(uuid.uuid4())
    
    request_id = state["request_id"]
    user_input = state.get("user_input", "")
    
    try:
        # Step 1: Redact NRICs
        sanitized_text, found_nrics = redact_nric(user_input, mode="partial")
        
        # Step 2: Flag prohibited content
        content_flags = contains_prohibited_keywords(sanitized_text)
        
        # Step 3: Build PDPA flags
        pdpa_flags = []
        if found_nrics:
            pdpa_flags.append("nric_found")
        if content_flags:
            pdpa_flags.extend(content_flags)
        
        # Step 4: Map to AI Verify principles
        ai_verify_principles = ["P2_Safety", "P9_Accountability"]
        if found_nrics:
            ai_verify_principles.append("P1_Transparency")  # User should know we redacted
        
        # Step 5: Update state
        state["sanitized_input"] = sanitized_text
        state["pdpa_flags"] = pdpa_flags
        state["ai_verify_principles"] = ai_verify_principles
        state["error"] = None
        
        # Step 6: Audit log
        execution_time = int((time.time() - start_time) * 1000)
        
        logger.log_node_execution(
            request_id=request_id,
            node_name="input_sanitizer",
            input_hash=hash_pii(user_input),
            output_hash=hash_pii(sanitized_text),
            pdpa_flags=pdpa_flags,
            ai_verify_principles=ai_verify_principles,
            execution_time_ms=execution_time,
            metadata={
                "nric_count": len(found_nrics),
                "redaction_mode": "partial"
            }
        )
        
        print(f"✅ Node 1 Complete: {len(found_nrics)} NRICs redacted")
        
    except Exception as e:
        # Fail gracefully
        state["error"] = f"Input sanitizer failed: {str(e)}"
        state["sanitized_input"] = user_input  # Pass through on error
        
        logger.log_node_execution(
            request_id=request_id,
            node_name="input_sanitizer",
            input_hash=hash_pii(user_input),
            output_hash=None,
            pdpa_flags=["error"],
            ai_verify_principles=["P9_Accountability"],
            execution_time_ms=int((time.time() - start_time) * 1000),
            error_message=str(e)
        )
        
        print(f"❌ Node 1 Error: {e}")
    
    return state