# tools/fuzzy_clean.py - Centrale, simpele en robuuste clean logica
import sys
import re
import unicodedata

def fuzzy_clean(text):
    if not text:
        return ""

    # Frontmatter strippen
    text = re.sub(r'^---\s*\n[\s\S]*?\n---\s*\n', '', text, flags=re.MULTILINE)

    t = unicodedata.normalize("NFKC", text)

    # Markdown stripping (geen titels meer strippen)
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

    # Normaliseren
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t

if __name__ == "__main__":
    text = sys.stdin.read()
    print(fuzzy_clean(text), end="")