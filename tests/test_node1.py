"""
Test Node 1: Input Sanitizer
Run this to verify NRIC redaction and audit logging
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nodes.node_1_input_sanitizer import input_sanitizer_node, GraphState

# Test Case 1: Clean input (no PII)
print("=" * 60)
print("TEST 1: Clean Input")
print("=" * 60)

state1: GraphState = {
    "request_id": "",
    "user_input": "What are the requirements for a police report?",
    "sanitized_input": "",
    "pdpa_flags": [],
    "ai_verify_principles": [],
    "error": ""
}

result1 = input_sanitizer_node(state1)
print(f"Input: {result1['user_input']}")
print(f"Sanitized: {result1['sanitized_input']}")
print(f"PDPA Flags: {result1['pdpa_flags']}")
print(f"AI Verify: {result1['ai_verify_principles']}")
print(f"Request ID: {result1['request_id']}\n")

# Test Case 2: Input with NRIC
print("=" * 60)
print("TEST 2: Input with NRIC")
print("=" * 60)

state2: GraphState = {
    "request_id": "",
    "user_input": "My NRIC is S1234567A and I need to file a report.",
    "sanitized_input": "",
    "pdpa_flags": [],
    "ai_verify_principles": [],
    "error": ""
}

result2 = input_sanitizer_node(state2)
print(f"Input: {result2['user_input']}")
print(f"Sanitized: {result2['sanitized_input']}")
print(f"PDPA Flags: {result2['pdpa_flags']}")
print(f"AI Verify: {result2['ai_verify_principles']}\n")

# Test Case 3: Input with prohibited content
print("=" * 60)
print("TEST 3: Medical Data Flag")
print("=" * 60)

state3: GraphState = {
    "request_id": "",
    "user_input": "I need my medical record for NRIC S9876543B",
    "sanitized_input": "",
    "pdpa_flags": [],
    "ai_verify_principles": [],
    "error": ""
}

result3 = input_sanitizer_node(state3)
print(f"Input: {result3['user_input']}")
print(f"Sanitized: {result3['sanitized_input']}")
print(f"PDPA Flags: {result3['pdpa_flags']}")
print(f"AI Verify: {result3['ai_verify_principles']}\n")

print("=" * 60)
print("✅ All tests complete. Check BigQuery for audit logs.")
print("=" * 60)