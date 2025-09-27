#!/usr/bin/env python3
"""
Run the exact test from the test file with debugging.
"""

import sys
sys.path.insert(0, '/workspace')

from prompted_objects.docstring_parser import DocstringParser
from prompted_objects.exceptions import ValidationError

def test_simple_metadata_only():
    """Test parsing docstring with only METADATA section."""
    parser = DocstringParser()

    # Exact docstring from the failing test
    docstring = '''
METADATA:
key: value
another: 123
'''

    print("About to parse docstring:")
    print(repr(docstring))

    # Let's add some debugging to the parser call
    print("\nDebugging parser steps:")

    # Clean the docstring
    cleaned_docstring = parser._clean_docstring(docstring)
    print(f"Cleaned: {repr(cleaned_docstring)}")

    # Find sections
    sections = parser._find_sections(cleaned_docstring)
    print(f"Sections: {sections}")

    # Extract metadata content
    metadata_content = parser._extract_section_content(cleaned_docstring, sections, "METADATA")
    print(f"Metadata content: {repr(metadata_content)}")

    # Try parsing the metadata
    print("\nTrying to parse metadata with yaml:")
    import yaml
    try:
        parsed_metadata = yaml.safe_load(metadata_content) or {}
        print(f"YAML result: {parsed_metadata}")
    except Exception as e:
        print(f"YAML error: {e}")
        import traceback
        traceback.print_exc()

    # Now try the full parse
    print("\nTrying full parse:")
    try:
        result = parser.parse(docstring)
        print(f"Full result: {result.metadata}")
        assert result.prompt is None
        assert result.metadata == {"key": "value", "another": 123}
        assert result.notes is None
        print("✓ Test passed!")
    except Exception as e:
        print(f"Full parse error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_metadata_only()