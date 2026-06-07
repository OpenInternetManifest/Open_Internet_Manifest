#!/usr/bin/env python3
# tools/debug-hr-locations.py - Toon exacte locaties van ---

import sys
import re
from pathlib import Path

def debug_hr(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"\n=== {filepath.name} ===")
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '---':
            context = '\n'.join(lines[max(0, i-2):i+3])
            print(f"Lijn {i+1:3d}: ---")
            print("Context:")
            print(context)
            print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python3 tools/debug-hr-locations.py <bestand.md>")
        sys.exit(1)
    
    debug_hr(Path(sys.argv[1]))