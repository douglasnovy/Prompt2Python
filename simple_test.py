#!/usr/bin/env python3
"""
Simple test without any framework.
"""

import sys
sys.path.insert(0, '/workspace')

def test_docstring_parser():
    from prompted_objects.docstring_parser import DocstringParser

    parser = DocstringParser()

    # Test cases
    test_cases = [
        # Test 1: Simple prompt
        {
            'name': 'Simple prompt',
            'docstring': '''
PROMPT:
This is a test prompt.
''',
            'expected_prompt': 'This is a test prompt.',
            'expected_metadata': {},
            'expected_notes': None
        },

        # Test 2: Simple metadata (the failing one)
        {
            'name': 'Simple metadata',
            'docstring': '''
METADATA:
key: value
another: 123
''',
            'expected_prompt': None,
            'expected_metadata': {'key': 'value', 'another': 123},
            'expected_notes': None
        },

        # Test 3: All sections
        {
            'name': 'All sections',
            'docstring': '''
PROMPT:
This is the prompt section.

METADATA:
id: test.function
policy:
  - if: "is_int(a)"
    then: code

NOTES:
Additional documentation here.
''',
            'expected_prompt': 'This is the prompt section.',
            'expected_metadata': {
                'id': 'test.function',
                'policy': [{'if': 'is_int(a)', 'then': 'code'}]
            },
            'expected_notes': 'Additional documentation here.'
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"Running test {i}: {test_case['name']}")
        try:
            result = parser.parse(test_case['docstring'])

            # Check results
            assert result.prompt == test_case['expected_prompt'], f"Prompt mismatch: {result.prompt} != {test_case['expected_prompt']}"
            assert result.metadata == test_case['expected_metadata'], f"Metadata mismatch: {result.metadata} != {test_case['expected_metadata']}"
            assert result.notes == test_case['expected_notes'], f"Notes mismatch: {result.notes} != {test_case['expected_notes']}"

            print(f"✓ Test {i} passed")

        except Exception as e:
            print(f"✗ Test {i} failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    return True

if __name__ == "__main__":
    success = test_docstring_parser()
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)