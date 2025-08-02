import os
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

from selector import choose_prompt_and_manual
from prompt_engine.prompt_loader import load_prompt_and_raster
from prompt_engine.openai_request import send_prompt_with_retry
from prompt_engine.evaluation import extract_score, save_md_file, build_result_row
from prompt_engine.excel_io import load_input_excel, save_results_excel, format_excel_columns

# Debug-Modus
DEBUG = True

# .env laden
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY nicht gefunden (.env prüfen)")

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
        raise FileNotFoundError(f"{name} nicht gefunden: {path}")

# Excel einlesen
data_df = load_input_excel(DATA_PATH)

# Prompt & Raster laden
raw_prompt, raster_text = load_prompt_and_raster(PROMPT_PATH, RASTER_PATH)

# Fortschrittsanzeige vorbereiten
results = []
progress_bar = tqdm(total=len(data_df), desc="Verarbeitung", ncols=100)

for idx, row in enumerate(data_df.itertuples(index=False), 1):
    textantwort = str(row.Textfeld).strip()
    beschreibung = ""

    if not textantwort or textantwort.lower() in {"nan", "none", "[leer]"}:
        print(f"Zeile {idx} übersprungen – leere oder ungültige Eingabe.")
        progress_bar.update(1)
        continue

    # Prompt erzeugen
    prompt_text = (
        raw_prompt
        .replace("{{TEXT}}", textantwort)
        .replace("{{RASTER}}", raster_text)
        .replace("{{BESCHREIBUNG}}", beschreibung)
    )

    try:
        antwort, refusal_detected = send_prompt_with_retry(client, prompt_text, idx)

        punktzahl = None
        if not refusal_detected:
            punktzahl = extract_score(antwort)

        save_md_file(idx, antwort, OUTPUT_DIR)
        results.append(build_result_row(textantwort, antwort, punktzahl))

    except Exception as e:
        print(f"--- Fehler bei Zeile {idx} ---")
        print(str(e))
        with open(OUTPUT_DIR / f"{idx}_error.txt", "w", encoding="utf-8") as f:
            f.write(str(e))

    progress_bar.update(1)
    time.sleep(1)

# Excel exportieren und formatieren
excel_path = OUTPUT_DIR / "auswertung.xlsx"
save_results_excel(results, excel_path)
format_excel_columns(excel_path)

print(f"\nExcel-Datei gespeichert unter: {excel_path}")
print("Formatierung angewendet (Zeilenumbruch + Spaltenbreiten)")