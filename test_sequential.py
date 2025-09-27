#!/usr/bin/env python3
"""
Run tests sequentially to find which one is failing.
"""

import sys
sys.path.insert(0, '/workspace')

from prompted_objects.docstring_parser import DocstringParser, parse_docstring
from prompted_objects.exceptions import ValidationError

def test_1():
    """Test 1: Simple prompt parsing"""
    parser = DocstringParser()
    docstring = '''
    PROMPT:
    This is a test prompt.
    '''
    result = parser.parse(docstring)
    assert result.prompt == "This is a test prompt."
    assert result.metadata == {}
    assert result.notes is None
    print("✓ Test 1 passed")

def test_2():
    """Test 2: Simple metadata parsing"""
    parser = DocstringParser()
    docstring = '''
    METADATA:
    key: value
    another: 123
    '''
    result = parser.parse(docstring)
    assert result.prompt is None
    assert result.metadata == {"key": "value", "another": 123}
    assert result.notes is None
    print("✓ Test 2 passed")

def test_3():
    """Test 3: All sections"""
    parser = DocstringParser()
    docstring = '''
    PROMPT:
    This is the prompt section.

    METADATA:
    id: test.function
    policy:
      - if: "is_int(a)"
        then: code

    NOTES:
    Additional documentation here.
    '''
    result = parser.parse(docstring)
    assert result.prompt == "This is the prompt section."
    assert result.metadata == {
        "id": "test.function",
        "policy": [{"if": "is_int(a)", "then": "code"}]
    }
    assert result.notes == "Additional documentation here."
    print("✓ Test 3 passed")

if __name__ == "__main__":
    try:
        test_1()
        test_2()
        test_3()
        print("All sequential tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)