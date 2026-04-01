"""
NRIC Sanitizer - PDPA Compliance Module
Redacts Singapore NRICs according to Personal Data Protection Act 2012
"""

import re
import hashlib
from typing import Tuple, List

# Singapore NRIC/FIN regex pattern
# Format: [STFGM]xxxxxxx[A-Z] where x is a digit
NRIC_PATTERN = re.compile(
    r'\b[STFGM]\d{7}[A-Z]\b',
    re.IGNORECASE
)

def redact_nric(text: str, mode: str = "partial") -> Tuple[str, List[str]]:
    """
    Redact NRICs from text according to PDPA guidelines.
    
    Args:
        text: Input text potentially containing NRICs
        mode: 'partial' (S****567A) or 'full' (S*******A)
    
    Returns:
        Tuple of (redacted_text, list_of_found_nrics)
    
    PDPA Mapping:
        - Section 24: Purpose Limitation (redact unless necessary)
        - Section 25: Consent (assume no consent for display)
    
    AI Verify Mapping:
        - P2: Safety (prevent identity exposure)
        - P9: Accountability (log what was redacted)
    """
    found_nrics = []
    
    def redact_match(match):
        nric = match.group(0).upper()
        found_nrics.append(nric)
        
        if mode == "full":
            # S*******A
            return f"{nric[0]}{'*' * 7}{nric[-1]}"
        else:
            # S****567A (show last 3 digits for verification)
            return f"{nric[0]}{'*' * 4}{nric[4:7]}{nric[-1]}"
    
    redacted_text = NRIC_PATTERN.sub(redact_match, text)
    
    return redacted_text, found_nrics


def hash_pii(data: str) -> str:
    """
    Create a SHA-256 hash of PII for audit logging.
    Allows verification without storing actual data.
    
    AI Verify P9: Accountability (audit trail without exposing PII)
    """
    return hashlib.sha256(data.encode()).hexdigest()[:16]


def contains_prohibited_keywords(text: str) -> List[str]:
    """
    Flag content that may violate PDPA purpose limitation.
    
    Returns list of flags (e.g., ['medical_data', 'financial_data'])
    """
    flags = []
    
    # Medical data patterns
    medical_keywords = [
        r'\bmedical record\b', r'\bdiagnosis\b', r'\bprescription\b',
        r'\bhospital\b', r'\bdoctor\b', r'\bpatient\b'
    ]
    
    # Financial data patterns
    financial_keywords = [
        r'\bcredit card\b', r'\bbank account\b', r'\bCVV\b',
        r'\bsalary\b', r'\bincome\b'
    ]
    
    text_lower = text.lower()
    
    if any(re.search(pattern, text_lower) for pattern in medical_keywords):
        flags.append('medical_data')
    
    if any(re.search(pattern, text_lower) for pattern in financial_keywords):
        flags.append('financial_data')
    
    return flags