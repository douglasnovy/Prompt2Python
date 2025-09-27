#!/usr/bin/env python3
"""
Test just the failing test case.
"""

import sys
sys.path.insert(0, '/workspace')

from prompted_objects.docstring_parser import DocstringParser

parser = DocstringParser()

# Exact test case
docstring = '''
METADATA:
key: value
another: 123
'''

print("Testing docstring:")
print(repr(docstring))

try:
    result = parser.parse(docstring)
    print("Success! Result:", result.metadata)
    assert result.metadata == {"key": "value", "another": 123}
    print("Test passed!")
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()