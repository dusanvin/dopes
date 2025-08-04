import os
import time
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

from selector import choose_prompt_and_manual
from prompt_engine.prompt_loader import load_prompt_and_raster
from prompt_engine.openai_request import send_prompt_with_retry
from prompt_engine.evaluation import extract_score, build_result_row
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
OUTPUT_DIR = Path("responses/zero-shot")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
AUSWERTUNG_PATH = OUTPUT_DIR / "auswertung.xlsx"

# Dateien prüfen
for path, name in [(DATA_PATH, "Excel-Datei"), (PROMPT_PATH, "Prompt-Datei"), (RASTER_PATH, "Raster-Datei")]:
    if not path.exists():
        raise FileNotFoundError(f"{name} nicht gefunden: {path}")

# Eingabedaten laden
data_df = load_input_excel(DATA_PATH)
data_df["Id"] = data_df["Id"].astype(str)

# Vorhandene Auswertung laden
if AUSWERTUNG_PATH.exists():
    auswertung_df = pd.read_excel(AUSWERTUNG_PATH, dtype={"Id": str})
else:
    auswertung_df = pd.DataFrame(columns=["Id", "Textaufgabe", "Begruendung", "Punktzahl"])

# Nur Ids mit vergebener Punktzahl (also echte Bewertungen)
bereits_bewertet_ids = (
    auswertung_df[auswertung_df["Punktzahl"].notna() & (auswertung_df["Punktzahl"] != "")]
    .Id.astype(str)
    .unique()
    .tolist()
)

# Prompt & Raster laden
raw_prompt, raster_text = load_prompt_and_raster(PROMPT_PATH, RASTER_PATH)

# Fortschrittsanzeige vorbereiten
results = []
progress_bar = tqdm(total=len(data_df), desc="Verarbeitung", ncols=100)

for idx, row in enumerate(data_df.itertuples(index=False), 1):
    try:
        id_value = row.Id
        textantwort = str(row.Textfeld).strip()

        if id_value in bereits_bewertet_ids:
            print(f"Überspringe ID {id_value} – bereits bewertet.")
            progress_bar.update(1)
            continue

        if not textantwort or textantwort.lower() in {"nan", "none", "[leer]"}:
            print(f"Überspringe ID {id_value} – leere Eingabe.")
            progress_bar.update(1)
            continue

        # Prompt bauen
        prompt_text = (
            raw_prompt
            .replace("{{TEXT}}", textantwort)
            .replace("{{RASTER}}", raster_text)
            .replace("{{BESCHREIBUNG}}", "")
        )

        # Anfrage senden
        antwort, refusal_detected = send_prompt_with_retry(client, prompt_text, idx)

        punktzahl = None
        if not refusal_detected:
            punktzahl = extract_score(antwort)

        # Ergebnis speichern
        results.append(build_result_row(id_value, textantwort, antwort, punktzahl))

    except Exception as e:
        print(f"Fehler bei ID {id_value}")
        with open(OUTPUT_DIR / f"{id_value}_error.txt", "w", encoding="utf-8") as f:
            f.write(str(e))

    progress_bar.update(1)
    time.sleep(0.1)

# Ergebnisse speichern
if results:
    neue_df = pd.DataFrame(results)
    neue_df["Id"] = neue_df["Id"].astype(str)
    neue_df = neue_df[~neue_df["Id"].isin(bereits_bewertet_ids)]

    # Nur neue Bewertungen anhängen
    auswertung_df = pd.concat([auswertung_df, neue_df], ignore_index=True)

    # Optional: Duplikate auf Basis von "Id" entfernen (falls versehentlich doppelt)
    auswertung_df.drop_duplicates(subset=["Id"], keep="last", inplace=True)

    save_results_excel(auswertung_df, AUSWERTUNG_PATH)
    format_excel_columns(AUSWERTUNG_PATH)
    print(f"\nExcel-Datei gespeichert unter: {AUSWERTUNG_PATH}")
else:
    print("\nKeine neuen Bewertungen hinzugefügt.")

