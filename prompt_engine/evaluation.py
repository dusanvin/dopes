import re
from pathlib import Path

def extract_score(text):
    patterns = [
        r"\*\*Gesamtbewertung\*\*.*?\|[^0-9]*([0-9]+)\b",      # Markdown-Tabelle mit "**Gesamtbewertung**"
        r"Gesamtpunktzahl[:\s]+([0-9]+)\b",                    # Freitext wie "Gesamtpunktzahl: 15"
        r"\*\*Gesamtpunktzahl\*\*\s*\|\s*([0-9]+)",            # Markdown-Tabelle mit "**Gesamtpunktzahl**"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
    return None

def save_md_file(idx, antwort, output_dir: Path):
    output_file = output_dir / f"{idx}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(antwort)

def build_result_row(id_value, textantwort, begruendung, punktzahl):
    return {
        "Id": id_value,
        "Textaufgabe": textantwort,
        "Begruendung": begruendung,
        "Punktzahl": punktzahl,
    }

