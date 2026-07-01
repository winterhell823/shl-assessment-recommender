#!/usr/bin/env python3
"""Test script to verify the refusal behavior fix."""

from app.classifiers.intent_classifier import IntentClassifier
from app.utils.constants import IntentType

# Test cases from the user's requirements
test_cases = [
    # SHOULD RETURN RECOMMEND (currently broken)
    ("What assessments should I use for hiring a Mid-Level Frontend React Developer?", IntentType.RECOMMEND),
    ("What assessments should I use for hiring a Java developer?", IntentType.RECOMMEND),
    
    # SHOULD RETURN RECOMMEND
    ("Recommend tests for Java developer", IntentType.RECOMMEND),
    ("Need assessment for frontend engineer", IntentType.RECOMMEND),
    ("Best SHL assessment for accountant", IntentType.RECOMMEND),
    ("Assessments for DevOps engineer", IntentType.RECOMMEND),
    ("java developer", IntentType.RECOMMEND),
    
    # SHOULD RETURN REFUSE
    ("What salary should I offer a React developer?", IntentType.REFUSE),
    ("Give interview questions for Java developer", IntentType.REFUSE),
    
    # GREETINGS
    ("hi", IntentType.GREETING),
    ("hello", IntentType.GREETING),
]

classifier = IntentClassifier()
passed = 0
failed = 0

print("=" * 70)
print("TESTING REFUSAL BEHAVIOR FIX")
print("=" * 70)

for query, expected_intent in test_cases:
    result = classifier.classify(query)
    status = "✓ PASS" if result == expected_intent else "✗ FAIL"
    
    if result == expected_intent:
        passed += 1
    else:
        failed += 1
    
    print(f"\n{status}")
    print(f"Query:    '{query}'")
    print(f"Expected: {expected_intent.value}")
    print(f"Got:      {result.value}")

print("\n" + "=" * 70)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
print("=" * 70)

if failed == 0:
    print("✓ All tests passed!")
    exit(0)
else:
    print("✗ Some tests failed!")
    exit(1)
