import re
from pathlib import Path

def extract_score(text):
    match = re.search(r"\*\*Gesamtbewertung\*\*.*?\|[^0-9]*([0-5])\b", text)
    return int(match.group(1)) if match else None

def save_md_file(idx, antwort, output_dir: Path):
    output_file = output_dir / f"{idx}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(antwort)

def build_result_row(textantwort, antwort, punktzahl):
    return {
        "Textaufgabe": textantwort,
        "Begruendung": antwort,
        "Punktzahl": punktzahl
    }
