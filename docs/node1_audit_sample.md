# Node 1: Sample Audit Log Entry

This is what gets written to BigQuery for every execution.

---

## Sample Entry (Clean Input)
```json
{
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "timestamp": "2026-03-31T14:23:45.123456",
  "node_name": "input_sanitizer",
  "input_hash": "8f3a2b1c5d6e7f8a",
  "output_hash": "8f3a2b1c5d6e7f8a",
  "pdpa_flags": [],
  "ai_verify_principles": ["P2_Safety", "P9_Accountability"],
  "execution_time_ms": 12,
  "error_message": null,
  "metadata": "{\"nric_count\": 0, \"redaction_mode\": \"partial\"}"
}
```

---

## Sample Entry (NRIC Detected)
```json
{
  "request_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "timestamp": "2026-03-31T14:24:10.987654",
  "node_name": "input_sanitizer",
  "input_hash": "1a2b3c4d5e6f7890",
  "output_hash": "9f8e7d6c5b4a3210",
  "pdpa_flags": ["nric_found"],
  "ai_verify_principles": ["P2_Safety", "P9_Accountability", "P1_Transparency"],
  "execution_time_ms": 18,
  "error_message": null,
  "metadata": "{\"nric_count\": 1, \"redaction_mode\": \"partial\"}"
}
```

**Notice**: `input_hash ≠ output_hash` because input was modified (NRIC redacted).

---

## Sample Entry (Medical Data Flag)
```json
{
  "request_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "timestamp": "2026-03-31T14:25:33.555555",
  "node_name": "input_sanitizer",
  "input_hash": "2b3c4d5e6f7a8901",
  "output_hash": "a0b9c8d7e6f54321",
  "pdpa_flags": ["nric_found", "medical_data"],
  "ai_verify_principles": ["P2_Safety", "P9_Accountability", "P1_Transparency"],
  "execution_time_ms": 20,
  "error_message": null,
  "metadata": "{\"nric_count\": 1, \"redaction_mode\": \"partial\"}"
}
```

---

## Querying Audit Logs

### 1. Find all requests that triggered NRIC redaction (last 7 days)
```sql
-- Data scanned: ~5MB per 10,000 requests

SELECT 
    request_id,
    timestamp,
    JSON_EXTRACT_SCALAR(metadata, '$.nric_count') AS nric_count
FROM `nric-langgaph-audit.audit_trail.node_logs`
WHERE node_name = 'input_sanitizer'
    AND 'nric_found' IN UNNEST(pdpa_flags)
    AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY timestamp DESC;
```

### 2. Calculate average execution time by PDPA flag
```sql
-- Data scanned: ~10MB per 50,000 requests

SELECT 
    pdpa_flag,
    COUNT(*) AS request_count,
    AVG(execution_time_ms) AS avg_time_ms,
    MAX(execution_time_ms) AS max_time_ms
FROM `nric-langgaph-audit.audit_trail.node_logs`,
    UNNEST(pdpa_flags) AS pdpa_flag
WHERE node_name = 'input_sanitizer'
GROUP BY pdpa_flag
ORDER BY avg_time_ms DESC;
```

### 3. Detect potential attacks (prompt injection keywords)
```sql
-- Data scanned: ~2MB per 10,000 requests

SELECT 
    request_id,
    timestamp,
    error_message
FROM `nric-langgaph-audit.audit_trail.node_logs`
WHERE node_name = 'input_sanitizer'
    AND (
        LOWER(error_message) LIKE '%ignore%instructions%'
        OR LOWER(error_message) LIKE '%system%prompt%'
    )
ORDER BY timestamp DESC
LIMIT 50;
```