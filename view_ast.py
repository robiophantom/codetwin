#!/usr/bin/env python
"""
Simple script to display the AST tree structure for a Python file
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from codetwin.frontends.TS_Python import Python_AST

if len(sys.argv) < 2:
    print("Usage: python view_ast.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

print(f"\n{'='*60}")
print(f"AST for: {filename}")
print(f"{'='*60}\n")

try:
    ast = Python_AST.create(filename)
    ast.display()
    print(f"\n{'='*60}")
    print(f"Total nodes: {len(ast.preorder())}")
    print(f"{'='*60}\n")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
