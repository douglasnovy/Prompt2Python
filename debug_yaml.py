#!/usr/bin/env python3
"""
Debug script to see what's happening with YAML parsing.
"""

import sys
sys.path.insert(0, '/workspace')

from prompted_objects.docstring_parser import DocstringParser

parser = DocstringParser()

docstring = '''
METADATA:
key: value
another: 123
'''

result = parser.parse(docstring)
print("Metadata content:", repr(result.metadata))

# Let's also see what sections are found
sections = parser._find_sections(docstring.strip())
print("Sections found:", sections)

# And what content is extracted
metadata_content = parser._extract_section_content(docstring.strip(), sections, "METADATA")
print("Metadata content extracted:", repr(metadata_content))