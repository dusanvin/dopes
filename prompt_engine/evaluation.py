import re
from pathlib import Path

def extract_score(text):
    matches = re.findall(r"\b\d+\b", text)
    return int(matches[-1]) if matches else None

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
