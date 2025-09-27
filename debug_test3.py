#!/usr/bin/env python3
"""
Debug test 3 specifically.
"""

import sys
sys.path.insert(0, '/workspace')

from prompted_objects.docstring_parser import DocstringParser

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

print("Docstring:")
print(repr(docstring))

result = parser.parse(docstring)

print("\nResult:")
print(f"Prompt: {repr(result.prompt)}")
print(f"Metadata: {repr(result.metadata)}")
print(f"Notes: {repr(result.notes)}")

# Debug the metadata parsing specifically
cleaned = parser._clean_docstring(docstring)
sections = parser._find_sections(cleaned)
metadata_content = parser._extract_section_content(cleaned, sections, "METADATA")

print("\nMetadata content:")
print(repr(metadata_content))

print("\nTrying YAML parsing:")
import yaml
try:
    parsed = yaml.safe_load(metadata_content)
    print("Parsed:", repr(parsed))
except Exception as e:
    print("Error:", e)
    print("Let's try to debug the YAML structure:")
    lines = metadata_content.split('\n')
    for i, line in enumerate(lines):
        print(f"Line {i}: {repr(line)}")