#!/usr/bin/env python3
"""
Test with complete isolation - fresh imports for each test.
"""

import sys
import importlib

def run_test():
    # Fresh import for each test
    if 'prompted_objects' in sys.modules:
        del sys.modules['prompted_objects']
    if 'prompted_objects.docstring_parser' in sys.modules:
        del sys.modules['prompted_objects.docstring_parser']
    if 'prompted_objects.exceptions' in sys.modules:
        del sys.modules['prompted_objects.exceptions']

    from prompted_objects.docstring_parser import DocstringParser
    from prompted_objects.exceptions import ValidationError

    parser = DocstringParser()

    # Test the exact case that's failing
    docstring = '''
METADATA:
key: value
another: 123
'''

    try:
        result = parser.parse(docstring)
        print("Success! Result:", result.metadata)
        assert result.metadata == {"key": "value", "another": 123}
        print("Test passed!")
        return True
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_test()
    if not success:
        sys.exit(1)