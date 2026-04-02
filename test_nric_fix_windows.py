"""
Quick Test Script for NRIC Sanitizer Fix
Tests VUL-001 (Spaced NRICs) and VUL-002 (Hyphenated NRICs)

This version works with your project structure.
"""

import sys
import os

# Add the src directory to Python path
# This assumes your nric_sanitizer.py is in src/utils/
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

try:
    # Try importing from src.utils package structure
    from utils.nric_sanitizer import redact_nric
    print("✅ Successfully imported from src.utils.nric_sanitizer")
except ImportError:
    try:
        # Try importing if nric_sanitizer.py is in project root
        from nric_sanitizer import redact_nric
        print("✅ Successfully imported from nric_sanitizer")
    except ImportError:
        print("❌ ERROR: Cannot find nric_sanitizer module")
        print(f"\nSearching in:")
        print(f"  - {os.path.join(project_root, 'src', 'utils', 'nric_sanitizer.py')}")
        print(f"  - {os.path.join(project_root, 'nric_sanitizer.py')}")
        print(f"\nCurrent directory: {os.getcwd()}")
        print(f"Project root: {project_root}")
        print(f"\nPlease ensure nric_sanitizer.py is in one of these locations.")
        sys.exit(1)

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

print("\n" + "=" * 70)
print("NRIC SANITIZER FIX VERIFICATION")
print("=" * 70)
print()

passed = 0
failed = 0

for input_text, expected_output, description in test_cases:
    try:
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
        if found_nrics:
            print(f"  Found:    {found_nrics}")
        print()
    except Exception as e:
        print(f"❌ ERROR - {description}")
        print(f"  Exception: {e}")
        print()
        failed += 1

print("=" * 70)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
print("=" * 70)

if failed == 0:
    print("\n✅ ALL TESTS PASSED - VUL-001 and VUL-002 are FIXED!")
    print("\nNext steps:")
    print("1. Run the full red-team test suite: python tests\\redteam_node1.py")
    print("2. Update vulnerability register and README.md")
    print("3. Commit your changes")
    sys.exit(0)
else:
    print(f"\n❌ {failed} TESTS FAILED - Review the output above")
    sys.exit(1)
