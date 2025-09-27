#!/usr/bin/env python3
"""
Debug the YAML parsing issue more carefully.
"""

import sys
sys.path.insert(0, '/workspace')

from prompted_objects.docstring_parser import DocstringParser

# Create a fresh parser for each test
parser = DocstringParser()

docstring = '''
METADATA:
key: value
another: 123
'''

print("Original docstring:")
print(repr(docstring))

# Let's see the cleaned docstring
cleaned = parser._clean_docstring(docstring)
print("\nCleaned docstring:")
print(repr(cleaned))

# Let's see the sections
sections = parser._find_sections(cleaned)
print("\nSections found:", sections)

# Let's see the extracted metadata content
metadata_content = parser._extract_section_content(cleaned, sections, "METADATA")
print("\nMetadata content extracted:")
print(repr(metadata_content))

# Let's examine each character
print("\nCharacter analysis:")
for i, char in enumerate(metadata_content):
    print(f"{i}: {repr(char)} (ord: {ord(char)})")

print("\nTrying YAML parsing:")
import yaml
try:
    result = yaml.safe_load(metadata_content)
    print("Success:", result)
except Exception as e:
    print("Error:", e)
    print("Error position info:")
    # Try to show context around the error
    lines = metadata_content.split('\n')
    for i, line in enumerate(lines):
        print(f"Line {i}: {repr(line)}")