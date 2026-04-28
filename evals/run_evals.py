import json
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from triage import triage_email

with open('evals/test_cases.json', encoding='utf-8') as f:
    cases = json.load(f)

passed = 0
print(f"{'ID':<4} {'Type':<40} {'Expected':<15} {'Got':<15} {'Pass?'}")
print('-' * 85)

for case in cases:
    time.sleep(20)  # wait 3 seconds between calls to avoid rate limit
    result = triage_email(case['input'])
    if result.get('validation_failed'):
        got_intent = 'SCHEMA_ERROR'
        got_oos = None
    else:
        got_intent = result['intent']
        got_oos = result['out_of_scope']

    exp_intent = case['expected_intent']
    exp_oos = case['expected_out_of_scope']
    ok = (got_intent == exp_intent) and (got_oos == exp_oos)
    if ok:
        passed += 1
    status = 'PASS' if ok else 'FAIL'
    print(f"{case['id']:<4} {case['type']:<40} {exp_intent:<15} {got_intent:<15} {status}")

print(f"\nScore: {passed}/{len(cases)}")