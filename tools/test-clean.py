#!/usr/bin/env python3
# test-clean.py - Vergelijkt beide clean methodes

import sys
import re
import unicodedata
from hashlib import sha256

# === CENTRALE CLEAN (uit fuzzy_clean.py) ===
def central_clean(text):
    if not text:
        return ""
    t = unicodedata.normalize("NFKC", text)
    
    t = re.sub(r"^(dank dat je|lees zelf|check zelf|weiger mee te spelen|oim-uitweg|vraag aan jou)[:\s]+", "", t, flags=re.IGNORECASE|re.MULTILINE)
    
    t = re.sub(r"\*\*(.*?)\*\*", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"__(.*?)__", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"\*(.*?)\*", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"_(.*?)_", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"^#{1,6}\s+", "", t, flags=re.MULTILINE)
    t = re.sub(r"^>\s*", "", t, flags=re.MULTILINE)
    t = re.sub(r"^\s*[-*+]\s+", " ", t, flags=re.MULTILINE)
    t = re.sub(r"^\s*\d+\.\s+", " ", t, flags=re.MULTILINE)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"!\[.*?\]\(.*?\)", "", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"^-{3,}\s*$", "", t, flags=re.MULTILINE)
    t = re.sub(r"<[^>]+>", "", t)
    
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t

# === HUIDIGE VERIFIER CLEAN (jouw huidige versie) ===
def verifier_clean(text):
    if not text:
        return ""
    t = unicodedata.normalize("NFKC", text)
    
    t = re.sub(r"^(narratief|realiteit|hoe werkt het|dank dat je|lees zelf|check zelf|weiger mee te spelen)[:\s]+", "", t, flags=re.IGNORECASE|re.MULTILINE)
    
    t = re.sub(r"\*\*(.*?)\*\*", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"__(.*?)__", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"\*(.*?)\*", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"_(.*?)_", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"^#{1,6}\s+", "", t, flags=re.MULTILINE)
    t = re.sub(r"^>\s*", "", t, flags=re.MULTILINE)
    t = re.sub(r"^\s*[-*+]\s+", " ", t, flags=re.MULTILINE)
    t = re.sub(r"^\s*\d+\.\s+", " ", t, flags=re.MULTILINE)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"!\[.*?\]\(.*?\)", "", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"^-{3,}\s*$", "", t, flags=re.MULTILINE)
    t = re.sub(r"<[^>]+>", "", t)
    
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t

if __name__ == "__main__":
    text = sys.stdin.read()
    
    central = central_clean(text)
    verifier = verifier_clean(text)
    
    print("=== CENTRAL CLEAN (fuzzy_clean.py) ===")
    print(central)
    print(f"Lengte: {len(central)}")
    
    print("\n=== VERIFIER CLEAN (huidig) ===")
    print(verifier)
    print(f"Lengte: {len(verifier)}")
    
    print("\n=== VERSCHIL ===")
    print(f"Lengte verschil: {len(central) - len(verifier)} karakters")
    
    print("\nCentral SHA256 :", sha256(central.encode('utf-8')).hexdigest())
    print("Verifier SHA256:", sha256(verifier.encode('utf-8')).hexdigest())