"""
Quick Test Script for NRIC Sanitizer Fix
Tests VUL-001 (Spaced NRICs) and VUL-002 (Hyphenated NRICs)
"""

import sys
import os

# Add project to path
sys.path.insert(0, '/mnt/project')

from nric_sanitizer import redact_nric

# Test cases
test_cases = [
    # (input, expected_output, description)
    ("S1234567A", "S****567A", "Standard NRIC"),
    ("s1234567a", "S****567A", "Lowercase NRIC"),
    ("S 1234 567 A", "S****567A", "Spaced NRIC (VUL-001)"),
    ("S-1234-567-A", "S****567A", "Hyphenated NRIC (VUL-002)"),
    ("S 1234-567 A", "S****567A", "Mixed spacing/hyphens"),
    ("My NRIC is S1234567A", "My NRIC is S****567A", "NRIC in sentence"),
    ("My NRIC is S 1234 567 A and I need help", "My NRIC is S****567A and I need help", "Spaced NRIC in sentence"),
    ("My NRIC S-1234-567-A is on file", "My NRIC S****567A is on file", "Hyphenated NRIC in sentence"),
    ("S1234567A and T9876543B", "S****567A and T****543B", "Multiple NRICs"),
]

print("=" * 70)
print("NRIC SANITIZER FIX VERIFICATION")
print("=" * 70)
print()

passed = 0
failed = 0

for input_text, expected_output, description in test_cases:
    redacted, found_nrics = redact_nric(input_text, mode="partial")
    
    if redacted == expected_output:
        status = "✅ PASS"
        passed += 1
    else:
        status = "❌ FAIL"
        failed += 1
    
    print(f"{status} - {description}")
    print(f"  Input:    {input_text}")
    print(f"  Expected: {expected_output}")
    print(f"  Got:      {redacted}")
    print(f"  Found:    {found_nrics}")
    print()

print("=" * 70)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
print("=" * 70)

if failed == 0:
    print("✅ ALL TESTS PASSED - VUL-001 and VUL-002 are FIXED!")
    sys.exit(0)
else:
    print("❌ SOME TESTS FAILED - Review the output above")
    sys.exit(1)
