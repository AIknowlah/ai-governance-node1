# Compliance with PDPC AI Guidelines (March 2024)

## Our Approach to Personal Data in AI Systems

### Data Minimisation (Para 7.1)
Before any personal data reaches our AI system (Gemini), we:
- Redact unnecessary PII (NRICs) via Node 1: Input Sanitizer
- Only pass sanitized data to downstream AI processing
- This reduces "unnecessary data protection and cyber threat risks"

### Pseudonymisation (Para 7.2)
Node 1 implements partial NRIC redaction:
- S1234567A → S****567A
- Preserves last 3 digits for verification
- Meets PDPC's recommendation to "pseudonymise or de-identify"

### Transparency (Para 10.3)
When Node 1 redacts data:
- System flags the modification (`P1_Transparency`)
- UI can inform users: "Your NRIC was automatically redacted"
- Written policies explain this practice

### Accountability (Para 10.1-10.2)
Every execution logged to BigQuery with:
- What was done (redaction)
- When it happened (timestamp)
- Why it was done (PDPA flags)
- Proof of action (input/output hashes)

## Compliance Statement
Node 1 operates as a **data protection control** before AI processing begins, implementing PDPC-recommended practices for data minimisation and pseudonymisation.