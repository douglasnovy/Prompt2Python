#!/usr/bin/env python3
"""
Simple test script to verify docstring parser functionality without pytest.
"""

import sys
import os

# Add the current directory to the path so we can import our module
sys.path.insert(0, '/workspace')

try:
    from prompted_objects.docstring_parser import DocstringParser, DocstringParseResult, parse_docstring
    from prompted_objects.exceptions import ValidationError
    print("✓ Successfully imported docstring parser modules")
except ImportError as e:
    print(f"✗ Failed to import modules: {e}")
    sys.exit(1)

def test_basic_functionality():
    """Test basic docstring parsing functionality."""
    parser = DocstringParser()

    # Test 1: Simple prompt
    docstring = '''
    PROMPT:
    This is a test prompt.
    '''
    result = parser.parse(docstring)
    assert result.prompt == "This is a test prompt."
    assert result.metadata == {}
    assert result.notes is None
    print("✓ Test 1 passed: Simple prompt parsing")

    # Test 2: Simple metadata
    docstring = '''
    METADATA:
    key: value
    another: 123
    '''
    result = parser.parse(docstring)
    assert result.prompt is None
    assert result.metadata == {"key": "value", "another": 123}
    assert result.notes is None
    print("✓ Test 2 passed: Simple metadata parsing")

    # Test 3: All sections
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
    print("✓ Test 3 passed: All sections parsing")

    # Test 4: Complex nested metadata
    docstring = '''
    METADATA:
    id: math.add
    policy:
      - if: "is_int(a) and is_int(b)"
        then: code
      - else: model
    examples:
      - input: {a: 2, b: 3}
        output: 5
    capabilities:
      io: false
      network: false
    '''
    result = parser.parse(docstring)
    expected_metadata = {
        "id": "math.add",
        "policy": [
            {"if": "is_int(a) and is_int(b)", "then": "code"},
            {"else": "model"}
        ],
        "examples": [{"input": {"a": 2, "b": 3}, "output": 5}],
        "capabilities": {"io": False, "network": False}
    }
    assert result.metadata == expected_metadata
    print("✓ Test 4 passed: Complex nested metadata")

    # Test 5: Error handling for invalid YAML
    docstring = '''
    METADATA:
    invalid: yaml: content:
      - with: [unclosed brackets
    '''
    try:
        parser.parse(docstring)
        assert False, "Should have raised ValidationError"
    except ValidationError:
        print("✓ Test 5 passed: Invalid YAML error handling")

    # Test 6: Case insensitive section names
    docstring = '''
    prompt:
    Test prompt

    metadata:
    key: value

    notes:
    Test notes
    '''
    result = parser.parse(docstring)
    assert result.prompt == "Test prompt"
    assert result.metadata == {"key": "value"}
    assert result.notes == "Test notes"
    print("✓ Test 6 passed: Case insensitive section names")

    # Test 7: Empty sections
    docstring = '''
    PROMPT:

    METADATA:
    key: value

    NOTES:
    '''
    result = parser.parse(docstring)
    assert result.prompt is None
    assert result.metadata == {"key": "value"}
    assert result.notes is None
    print("✓ Test 7 passed: Empty sections handling")

    # Test 8: Convenience function
    docstring = '''
    PROMPT:
    Test prompt

    METADATA:
    key: value
    '''
    result = parse_docstring(docstring)
    assert result.prompt == "Test prompt"
    assert result.metadata == {"key": "value"}
    print("✓ Test 8 passed: Convenience function")

def test_real_world_example():
    """Test parsing the real-world example from the README."""
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

    assert result.prompt == "Return the sum of a and b."
    assert result.metadata["id"] == "math.add"
    assert result.metadata["policy"] == [
        {"if": "is_int(a) and is_int(b)", "then": "code"},
        {"else": "model"}
    ]
    assert result.metadata["examples"] == [{"input": {"a": 2, "b": 3}, "output": 5}]
    assert result.metadata["capabilities"] == {
        "io": False,
        "network": False,
        "imports": ["math"]
    }
    assert result.metadata["parse"] == "auto"
    assert result.metadata["strict"] is False
    assert result.notes == "This function adds two numbers together."
    print("✓ Real-world example test passed")

if __name__ == "__main__":
    try:
        test_basic_functionality()
        test_real_world_example()
        print("\n🎉 All tests passed! Docstring parser is working correctly.")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)