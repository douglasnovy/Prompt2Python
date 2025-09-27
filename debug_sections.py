#!/usr/bin/env python3
"""
Debug the section finding with multiple sections.
"""

import sys
sys.path.insert(0, '/workspace')
import re

SECTION_PATTERN = re.compile(r"^(PROMPT|METADATA|NOTES):\s*$", re.MULTILINE)

def debug_find_sections(docstring: str):
    """Debug version of _find_sections."""
    sections = {}
    lines = docstring.split('\n')

    print(f"Full docstring: {repr(docstring)}")
    print(f"Number of lines: {len(lines)}")
    for i, line in enumerate(lines):
        print(f"Line {i}: {repr(line)}")

    current_section = None
    current_start = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        match = SECTION_PATTERN.match(stripped)
        if match:
            section_name = match.group(1).upper()
            print(f"\nFound section '{section_name}' at line {i}")

            # Save previous section if it exists
            if current_section:
                print(f"Saving section {current_section}: ({current_start}, {i})")
                sections[current_section] = (current_start, i)

            # Start new section
            current_section = section_name
            current_start = i + 1
            print(f"Starting new section {current_section}, content starts at line {current_start}")

    # Handle the last section
    if current_section:
        print(f"\nHandling last section {current_section}: ({current_start}, {len(lines)})")
        sections[current_section] = (current_start, len(lines))

    print(f"\nFinal sections: {sections}")
    return sections

# Test with the problematic docstring
docstring = '''PROMPT:
This is the prompt section.

METADATA:
id: test.function
policy:
  - if: "is_int(a)"
    then: code

NOTES:
Additional documentation here.'''

print("=== Testing with multiple sections ===")
sections = debug_find_sections(docstring)

# Test the extraction
lines = docstring.split('\n')
for section_name, (start, end) in sections.items():
    print(f"\n{section_name} section (lines {start}-{end}):")
    section_lines = lines[start:end]
    print(f"Content: {section_lines}")
    content = '\n'.join(section_lines).strip()
    print(f"Joined: {repr(content)}")