"""
NRIC Sanitizer - PDPA Compliance Module
Redacts Singapore NRICs according to Personal Data Protection Act 2012
"""

import re
import hashlib
from typing import Tuple, List

# Singapore NRIC/FIN regex pattern
# Format: [STFGM]xxxxxxx[A-Z] where x is a digit
# Now supports: S1234567A, s1234567a, S 1234 567 A, S-1234-567-A
NRIC_PATTERN = re.compile(
    r'\b[STFGM][\s\-]?\d[\s\-]?\d[\s\-]?\d[\s\-]?\d[\s\-]?\d[\s\-]?\d[\s\-]?\d[\s\-]?[A-Z]\b',
    re.IGNORECASE
)

def normalize_nric(nric_text: str) -> str:
    """
    Remove spaces and hyphens from NRIC to get canonical form.
    
    Args:
        nric_text: NRIC string potentially with spaces/hyphens
    
    Returns:
        Normalized NRIC (e.g., "S 1234 567 A" -> "S1234567A")
    
    Examples:
        >>> normalize_nric("S 1234 567 A")
        'S1234567A'
        >>> normalize_nric("S-1234-567-A")
        'S1234567A'
        >>> normalize_nric("S1234567A")
        'S1234567A'
    """
    # Remove all spaces and hyphens, then convert to uppercase
    return re.sub(r'[\s\-]', '', nric_text).upper()

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
        # Get the matched NRIC (may contain spaces/hyphens)
        nric_raw = match.group(0)
        
        # Normalize it (remove spaces/hyphens, uppercase)
        nric = normalize_nric(nric_raw)
        found_nrics.append(nric)
        
        if mode == "full":
            # S*******A
            return f"{nric[0]}{'*' * 7}{nric[-1]}"
        else:
            # S****567A (show last 3 digits for verification)
            return f"{nric[0]}{'*' * 4}{nric[5:8]}{nric[-1]}"
    
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