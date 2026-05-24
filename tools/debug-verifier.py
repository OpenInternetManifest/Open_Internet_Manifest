#!/usr/bin/env python3
# debug-verifier.py - Gebruikt exact dezelfde clean als fuzzy_clean.py

import sys
import subprocess
from hashlib import sha256

def get_fuzzy_clean(text):
    try:
        result = subprocess.run(
            ['python3', 'tools/fuzzy_clean.py'],
            input=text,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error: {e}")
        return ""

if __name__ == "__main__":
    print("=== VERIFIER DEBUG TOOL ===")
    print("Plak tekst hier (Ctrl+D om te eindigen):\n")
    
    text = sys.stdin.read()
    
    clean = get_fuzzy_clean(text)
    hash_value = sha256(clean.encode('utf-8')).hexdigest()
    
    print("\n=== FUZZY CLEANED TEXT ===")
    print(clean)
    print(f"\nCleaned length: {len(clean)} karakters")
    print(f"\nFuzzy SHA256: {hash_value}")
    print("========================================")