#!/usr/bin/env python3
"""
Debug the specific test case that's failing.
"""

import sys
sys.path.insert(0, '/workspace')

from prompted_objects.docstring_parser import DocstringParser

parser = DocstringParser()

# This is the exact docstring from the failing test
docstring = '''
METADATA:
key: value
another: 123
'''

print("Original docstring:")
print(repr(docstring))

cleaned = parser._clean_docstring(docstring)
print("\nCleaned docstring:")
print(repr(cleaned))

sections = parser._find_sections(cleaned)
print("\nSections found:", sections)

metadata_content = parser._extract_section_content(cleaned, sections, "METADATA")
print("\nMetadata content extracted:")
print(repr(metadata_content))

print("\nTrying to parse with yaml:")
import yaml
try:
    result = yaml.safe_load(metadata_content)
    print("YAML parsing result:", result)
except Exception as e:
    print("YAML parsing error:", e)

print("\nTrying full parse:")
try:
    result = parser.parse(docstring)
    print("Full parse result:", result.metadata)
except Exception as e:
    print("Full parse error:", e)