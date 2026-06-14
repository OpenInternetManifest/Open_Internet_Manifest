# tools/fuzzy_clean.py - Centrale, robuuste clean logica (verbeterd)

import sys
import re
import unicodedata

def fuzzy_clean(text):
    if not text:
        return ""

    # 1. Frontmatter strippen
    text = re.sub(r'^---\s*\n[\s\S]*?\n---\s*\n', '', text, flags=re.MULTILINE)

    t = unicodedata.normalize("NFKC", text)

    # 2. Sterke Markdown + opmaak stripping
    t = re.sub(r"\*\*(.*?)\*\*", r"\1", t, flags=re.DOTALL)   # bold
    t = re.sub(r"__(.*?)__", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"\*(.*?)\*", r"\1", t, flags=re.DOTALL)       # italic
    t = re.sub(r"_(.*?)_", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"^#{1,6}\s+", "", t, flags=re.MULTILINE)      # headers
    t = re.sub(r"^>\s*", "", t, flags=re.MULTILINE)           # blockquotes
    t = re.sub(r"^\s*[-*+]\s+", " ", t, flags=re.MULTILINE)   # bullets
    t = re.sub(r"^\s*\d+\.\s+", " ", t, flags=re.MULTILINE)   # numbered lists
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)            # links
    t = re.sub(r"!\[.*?\]\(.*?\)", "", t)                     # images
    t = re.sub(r"`([^`]+)`", r"\1", t)                        # inline code
    t = re.sub(r"^-{3,}\s*$", "", t, flags=re.MULTILINE)      # HR
    t = re.sub(r"<[^>]+>", "", t)                             # HTML

    # Extra agressief voor resterende rommel
    t = re.sub(r"[\*#_>]", "", t)                             # losse markdown karakters
    t = re.sub(r"\s+", " ", t).strip().lower()

    return t


if __name__ == "__main__":
    text = sys.stdin.read()
    print(fuzzy_clean(text), end="")