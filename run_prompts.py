import os
import base64
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
from tqdm import tqdm
import time

# ENV laden
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Pfade
DATA_PATH = Path("data/data.xlsx")
MANUAL_PATH = Path("manual/manual.pdf")
OUTPUT_DIR = Path("responses/zero-shot")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Excel-Daten laden
data_df = pd.read_excel(DATA_PATH)

# Spalten prüfen
if not {'Antwort', 'beschreibung_vortrag'}.issubset(data_df.columns):
    raise ValueError("Die Excel-Datei muss die Spalten 'Antwort' und 'beschreibung_vortrag' enthalten.")

# PDF-Datei base64-kodieren
with open(MANUAL_PATH, "rb") as f:
    base64_manual = base64.b64encode(f.read()).decode("utf-8")

# Fortschrittsbalken starten
progress_bar = tqdm(total=len(data_df), desc="Verarbeitung", ncols=100)

for idx, row in data_df.iterrows():
    progress_bar.update(1)

    textantwort = str(row["Antwort"]).strip()
    beschreibung = str(row["beschreibung_vortrag"]).strip() if pd.notna(row["beschreibung_vortrag"]) else ""

    # Baue die Eingabe für GPT
    input_block = [
        {
            "type": "input_file",
            "filename": "manual.pdf",
            "file_data": f"data:application/pdf;base64,{base64_manual}",
        },
        {
            "type": "input_text",
            "text": (
                "Bitte bewerte den folgenden Text anhand des Bewertungsrasters in der angehängten PDF-Datei.\n\n"
                f"**Beschreibung des Vortrags:**\n{beschreibung}\n\n"
                f"**Zu bewertender Text:**\n{textantwort}"
            ),
        },
    ]

    try:
        response = client.responses.create(
            model="gpt-4o",
            input=[{"role": "user", "content": input_block}]
        )
        antwort = response.output_text

        # Ausgabe anzeigen & speichern
        print(f"\n✅ GPT-Antwort für Zeile {idx+1}:\n{'-'*60}\n{antwort}\n{'-'*60}\n")
        output_file = OUTPUT_DIR / f"{idx+1}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(antwort)

    except Exception as e:
        print(f"❌ Fehler bei Zeile {idx+1}: {e}")

    time.sleep(0.01)  # für Fortschrittsanzeige
