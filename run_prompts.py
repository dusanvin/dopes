import os
import time
import re
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
from selector import choose_prompt_and_manual

# Debug-Modus
DEBUG = True

# .env laden
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("⚠️ OPENAI_API_KEY nicht gefunden (.env prüfen)")
client = OpenAI(api_key=api_key)

# Pfade
DATA_PATH = Path("data/data.xlsx")
PROMPT_PATH, RASTER_PATH = choose_prompt_and_manual()
RASTER_PATH = Path("manual/manual_(1)zsl+du.md")
OUTPUT_DIR = Path("responses/zero-shot")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Dateien prüfen
for path, name in [(DATA_PATH, "Excel-Datei"), (PROMPT_PATH, "Prompt-Datei"), (RASTER_PATH, "Raster-Datei")]:
    if not path.exists():
        raise FileNotFoundError(f"❌ {name} nicht gefunden: {path}")

# Excel einlesen
data_df = pd.read_excel(DATA_PATH)
if "Textfeld" not in data_df.columns:
    raise ValueError("❌ Die Excel-Datei muss eine Spalte namens 'Textfeld' enthalten.")

# Prompt & Raster laden
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    raw_prompt = f.read()
with open(RASTER_PATH, "r", encoding="utf-8") as f:
    raster_text = f.read()

# Fortschrittsanzeige
progress_bar = tqdm(total=len(data_df), desc="Verarbeitung", ncols=100)
results = []

for idx, row in data_df.iterrows():
    progress_bar.update(1)
    textantwort = str(row["Textfeld"]).strip()
    beschreibung = ""  # Optional

    if not textantwort or textantwort.lower() in {"nan", "none", "[leer]"}:
        print(f"⚠️ Zeile {idx+1} übersprungen – leere oder ungültige Eingabe.")
        continue

    # Prompt vorbereiten
    prompt_text = (
        raw_prompt
        .replace("{{TEXT}}", textantwort)
        .replace("{{RASTER}}", raster_text)
        .replace("{{BESCHREIBUNG}}", beschreibung)
    )

    if DEBUG:
        print(f"\n📤 Prompt für Zeile {idx+1} (erste 300 Zeichen):\n{'-'*60}\n{prompt_text[:300]}\n{'-'*60}\n")

    input_block = [
        {
            "type": "input_text",
            "text": prompt_text,
        }
    ]

    try:
        response = client.responses.create(
            model="gpt-4o",
            input=[{"role": "user", "content": input_block}]
        )
        antwort = response.output_text

        print(f"\n✅ GPT-Antwort für Zeile {idx+1}:\n{'-'*60}\n{antwort[:500]}\n{'-'*60}\n")

        # .md-Datei speichern
        output_file = OUTPUT_DIR / f"{idx+1}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(antwort)

        # Punktzahl extrahieren
        punktzahl = None
        match = re.search(r"\*\*Gesamtbewertung\*\*.*?\|[^0-9]*([0-5])\b", antwort)
        if match:
            punktzahl = int(match.group(1))
        else:
            print(f"⚠️ Punktzahl in Zeile {idx+1} konnte nicht extrahiert werden.")

        # Für Excel speichern
        results.append({
            "Textaufgabe": textantwort,
            "Begruendung": antwort,
            "Punktzahl": punktzahl
        })

    except Exception as e:
        print(f"❌ Fehler bei Zeile {idx+1}: {e}")
        error_file = OUTPUT_DIR / f"{idx+1}_error.txt"
        with open(error_file, "w", encoding="utf-8") as f:
            f.write(str(e))

    time.sleep(0.01)

# Excel exportieren
excel_path = OUTPUT_DIR / "auswertung.xlsx"
df = pd.DataFrame(results)
df.to_excel(excel_path, index=False)

# Formatierung (Zeilenumbruch + Spaltenbreite)
wb = load_workbook(excel_path)
ws = wb.active

for col in ws.columns:
    max_length = 0
    col_letter = get_column_letter(col[0].column)

    for cell in col:
        cell.alignment = Alignment(wrap_text=True)
        if cell.value:
            max_length = max(max_length, len(str(cell.value)))

    ws.column_dimensions[col_letter].width = min(max_length * 0.9, 100)

wb.save(excel_path)
print(f"\n📄 Excel-Datei gespeichert unter: {excel_path}")
print("📐 Formatierung angewendet (Zeilenumbruch + Spaltenbreiten)")
