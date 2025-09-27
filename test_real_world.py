#!/usr/bin/env python3
"""
Test the real-world example from the README.
"""

import sys
sys.path.insert(0, '/workspace')

from prompted_objects.docstring_parser import parse_docstring

docstring = '''
PROMPT:
Return the sum of a and b.

METADATA:
id: math.add
policy:
  - if: "is_int(a) and is_int(b)"
    then: code
  - else: model
examples:
  - input: {a: 2, b: 3}
    output: 5
  - input: {a: "hello", b: "world"}
    output: "helloworld"
capabilities:
  io: false
  network: false
  imports: ["math"]
parse: auto
strict: false

NOTES:
This function adds two numbers together.
'''

result = parse_docstring(docstring)

print("Parsed result:")
print(f"Prompt: {repr(result.prompt)}")
print(f"Metadata: {repr(result.metadata)}")
print(f"Notes: {repr(result.notes)}")

# Verify expected structure
expected_metadata = {
    'id': 'math.add',
    'policy': [
        {'if': 'is_int(a) and is_int(b)', 'then': 'code'},
        {'else': 'model'}
    ],
    'examples': [
        {'input': {'a': 2, 'b': 3}, 'output': 5},
        {'input': {'a': 'hello', 'b': 'world'}, 'output': 'helloworld'}
    ],
    'capabilities': {
        'io': False,
        'network': False,
        'imports': ['math']
    },
    'parse': 'auto',
    'strict': False
}

assert result.prompt == "Return the sum of a and b."
assert result.metadata == expected_metadata
assert result.notes == "This function adds two numbers together."

print("\n✓ Real-world example test passed!")