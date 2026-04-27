#!/usr/bin/env python3
"""
fuzzy_similarity.py - Similarity fallback voor als exacte hash faalt
"""

import sys
from difflib import SequenceMatcher

def fuzzy_clean(text):  # kopieer hier je huidige fuzzy_clean functie uit de andere scripts
    # ... (plak hier je volledige fuzzy_clean functie)
    pass  # vervang dit met je echte functie

def fuzzy_similarity(text1: str, text2: str):
    c1 = fuzzy_clean(text1)
    c2 = fuzzy_clean(text2)

    if c1 == c2:
        return 100, "100% exacte match"

    # Jaccard op woorden
    words1 = set(c1.split())
    words2 = set(c2.split())
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    jaccard = intersection / union if union > 0 else 0

    # Sequence similarity (karakter niveau)
    seq = SequenceMatcher(None, c1, c2).ratio()

    # Gewogen score (meer nadruk op woorden)
    score = (jaccard * 0.72) + (seq * 0.28)
    percentage = round(score * 100)

    if percentage >= 95:
        label = "Bijna identiek"
    elif percentage >= 85:
        label = "Zeer waarschijnlijk authentiek"
    elif percentage >= 70:
        label = "Waarschijnlijk dezelfde post"
    else:
        label = "Niet herkend"

    return percentage, label


# Voor direct testen
if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()
        print("Test similarity nog niet volledig geïmplementeerd")