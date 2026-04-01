# Node 1: Input Sanitizer - Governance Mapping

**Node Name**: `input_sanitizer`  
**Purpose**: Redact PII (NRICs) and flag prohibited content before processing  
**Data Residency**: Singapore (asia-southeast1)  
**Last Updated**: 2026-03-31

---

## PDPA Compliance Mapping

| **PDPA Section** | **Requirement** | **Implementation** | **Evidence** |
|------------------|-----------------|-------------------|--------------|
| **Section 24: Purpose Limitation** | Personal data collected shall be for a legitimate purpose | NRICs are redacted unless explicitly required for downstream processing | `redact_nric()` function, audit logs show `nric_found` flag |
| **Section 25: Consent** | Must obtain consent before collecting/using personal data | Assume no consent to display full NRICs; redact by default | Partial redaction (S****567A) allows verification without full exposure |
| **Section 26: Accuracy** | Personal data must be accurate and complete | Hash original input for audit trail; redacted version preserves last 3 digits for manual verification | `hash_pii()` function stores SHA-256 hash |

---

## AI Verify Principles Mapping

| **AI Verify Principle** | **Requirement** | **Implementation** | **Test Method** |
|-------------------------|-----------------|-------------------|----------------|
| **P1: Transparency** | Users should know when AI modifies their input | If NRIC is redacted, add `P1_Transparency` flag to audit log | Check BigQuery for `ai_verify_principles` field |
| **P2: Safety** | Prevent identity exposure and harm | NRICs redacted before LLM processing; medical/financial data flagged | Red-team test: Submit S1234567A, verify output is S****567A |
| **P9: Accountability** | Every decision must be auditable | All inputs/outputs hashed and logged to BigQuery with `request_id` | Query audit logs by `request_id` to reconstruct full session |

---

## Data Flow
```
User Input (Raw)
    ↓
[NRIC Detection] → Regex: [STFGM]\d{7}[A-Z]
    ↓
[Redaction] → S1234567A becomes S****567A
    ↓
[Content Flagging] → Check for medical/financial keywords
    ↓
[Audit Logging] → Write to BigQuery (asia-southeast1)
    ↓
Sanitized Output → Pass to next node
```

---

## Residual Risks

| **Risk** | **Likelihood** | **Impact** | **Mitigation** |
|----------|----------------|------------|----------------|
| Obfuscated NRIC (e.g., "S 1234 567A") | Medium | Medium | Enhanced regex patterns (Phase 2) |
| Non-Singapore IDs (e.g., Malaysian IC) | Low | Low | Add multi-country patterns if scope expands |
| BigQuery logging failure | Low | High | Fail gracefully; log to local file as backup |

---

## Cost Estimate

- **BigQuery Storage**: ~0.02 USD per GB per month (Singapore)
- **BigQuery Insert**: ~0.00001 USD per log entry
- **Expected Monthly Cost** (1000 requests/day): ~0.30 USD

---

## Audit Query (Verification)
```sql
-- Query to verify NRIC redaction is working
-- Data scanned: ~1MB per 1000 requests

SELECT 
    request_id,
    timestamp,
    node_name,
    pdpa_flags,
    ai_verify_principles,
    execution_time_ms
FROM `nric-langgaph-audit.audit_trail.node_logs`
WHERE node_name = 'input_sanitizer'
    AND 'nric_found' IN UNNEST(pdpa_flags)
ORDER BY timestamp DESC
LIMIT 100;
```