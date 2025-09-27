#!/usr/bin/env python3

from prompted_objects.codegen.static_checks import validate_ast
from prompted_objects.exceptions import ValidationError

# Test 1: print should fail
print("=== Test 1: print should fail ===")
body1 = '''
print("debug")
'''

try:
    validate_ast(body1)
    print("ERROR: Should have failed!")
except ValidationError as e:
    print('Message:', repr(str(e)))

# Test 2: os with io capability should pass
print("\n=== Test 2: os with io capability should pass ===")
body2 = '''
import os
return os.getcwd()
'''

capabilities = {"imports": ["os"], "io": True}
try:
    validate_ast(body2, capabilities)
    print("SUCCESS: Passed validation")
except ValidationError as e:
    print('FAILED: Message:', repr(str(e)))
    print('Details:', e.details)

# Test 3: complexity limit (same as test)
print("\n=== Test 3: complexity limit (same as test) ===")
body3 = """
if True:
    if True:
        if True:
            if True:
                if True:
                    if True:
                        if True:
                            if True:
                                if True:
                                    if True:
                                        if True:
                                            if True:
                                                if True:
                                                    return 1
return 0
"""
try:
    validate_ast(body3)
    print("ERROR: Should have failed with complexity!")
except ValidationError as e:
    print('Message:', repr(str(e)))

# Test 4: check depth calculation
print("\n=== Test 4: check depth calculation ===")
import ast
from prompted_objects.codegen.static_checks import get_max_nesting_depth

tree = ast.parse(body3, mode='exec')
depth = get_max_nesting_depth(tree)
print(f"Calculated depth: {depth}")
node_count = 0
for node in ast.walk(tree):
    node_count += 1
print(f"Node count: {node_count}")
