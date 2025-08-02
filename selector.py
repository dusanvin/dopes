import os
import json
from pathlib import Path

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def list_files_in_directory(directory: Path, file_extension=".md"):
    return sorted([f for f in directory.glob(f"*{file_extension}") if f.is_file()])

def load_language_strings(language_code: str):
    lang_file = Path(f"lang/{language_code}.json")
    if not lang_file.exists():
        language_code = "de"
        lang_file = Path("lang/de.json")
    with open(lang_file, encoding="utf-8") as f:
        return json.load(f)

def choose_from_list(items, label, lang_strings):
    print(f"\n{lang_strings[f'select_{label}']}")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item.name}")
    while True:
        try:
            choice = int(input(lang_strings["enter_number"].format(max=len(items))))
            if 1 <= choice <= len(items):
                return items[choice - 1]
        except ValueError:
            pass
        print(lang_strings["invalid_input"])

def choose_prompt_and_manual():
    # Konsole leeren
    clear_console()

    # Sprache wählen – erster Satz auf Englisch
    print("Please select your language:")
    language = input("Enter 'de' for German or 'en' for English: ").strip().lower()
    if language not in {"de", "en"}:
        print("Invalid language, defaulting to German")
        language = "de"

    lang_strings = load_language_strings(language)

    # Prompt wählen
    prompt_dir = Path(f"prompts/{language}/zero-shot")
    prompts = list_files_in_directory(prompt_dir)
    if not prompts:
        raise FileNotFoundError(f"No prompt files found in {prompt_dir}")
    chosen_prompt = choose_from_list(prompts, "prompt", lang_strings)

    # Manual wählen
    manual_dir = Path("manual")
    manuals = list_files_in_directory(manual_dir)
    if not manuals:
        raise FileNotFoundError("No manual files found in manual/")
    chosen_manual = choose_from_list(manuals, "manual", lang_strings)

    return chosen_prompt, chosen_manual
