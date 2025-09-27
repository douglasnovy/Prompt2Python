#!/usr/bin/env python3
"""
Debug the section finding logic in detail.
"""

import sys
sys.path.insert(0, '/workspace')
import re

# Copy the exact logic from the parser
SECTION_PATTERN = re.compile(r"^(\w+):\s*$", re.MULTILINE)

def debug_find_sections(docstring: str):
    """Debug version of _find_sections."""
    sections = {}
    lines = docstring.split('\n')

    print(f"Docstring: {repr(docstring)}")
    print(f"Lines: {lines}")
    print(f"Number of lines: {len(lines)}")

    current_section = None
    current_start = 0

    for i, line in enumerate(lines):
        print(f"Line {i}: {repr(line)}")
        stripped = line.strip()
        print(f"  Stripped: {repr(stripped)}")
        match = SECTION_PATTERN.match(stripped)
        print(f"  Matches pattern: {match is not None}")
        if match:
            section_name = match.group(1).upper()
            print(f"  Section name: {section_name}")

            # Save previous section if it exists
            if current_section:
                print(f"  Saving previous section {current_section}: ({current_start}, {i})")
                sections[current_section] = (current_start, i)

            # Start new section
            current_section = section_name
            current_start = i + 1  # Content starts on next line
            print(f"  Starting new section {current_section}, content starts at line {current_start}")

    # Handle the last section
    if current_section:
        print(f"Handling last section {current_section}: ({current_start}, {len(lines)})")
        sections[current_section] = (current_start, len(lines))

    print(f"Final sections: {sections}")
    return sections

# Test with the problematic docstring
docstring = '''METADATA:
key: value
another: 123'''

print("=== Testing with the problematic docstring ===")
sections = debug_find_sections(docstring)
print()

# Now let's see what content would be extracted
lines = docstring.split('\n')
start_line, end_line = sections.get('METADATA', (0, 0))
print(f"Extracting from line {start_line} to {end_line}")
section_lines = lines[start_line:end_line]
print(f"Section lines: {section_lines}")
content = '\n'.join(section_lines).strip()
print(f"Final content: {repr(content)}")