import os
from pathlib import Path

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def list_files_in_directory(directory: Path, file_extension=".md"):
    return sorted([f for f in directory.glob(f"*{file_extension}") if f.is_file()])

def choose_from_list(items, label):
    print(f"\nSelect a {label}:")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item.name}")
    while True:
        try:
            choice = int(input(f"Enter number (1-{len(items)}): "))
            if 1 <= choice <= len(items):
                return items[choice - 1]
        except ValueError:
            pass
        print("Invalid input. Try again.")

def choose_prompt_and_manual():
    # Konsole leeren
    clear_console()

    # Sprache wählen
    print("Please select your language / Bitte Sprache wählen:")
    language = input("Enter 'de' for German or 'en' for English: ").strip().lower()
    if language not in {"de", "en"}:
        print("Invalid language, defaulting to 'de'")
        language = "de"

    # Prompt wählen
    prompt_dir = Path(f"prompts/{language}/zero-shot")
    prompts = list_files_in_directory(prompt_dir)
    if not prompts:
        raise FileNotFoundError(f"No prompt files found in {prompt_dir}")
    chosen_prompt = choose_from_list(prompts, "prompt")

    # Manual wählen
    manual_dir = Path("manual")
    manuals = list_files_in_directory(manual_dir)
    if not manuals:
        raise FileNotFoundError("No manual files found in manual/")
    chosen_manual = choose_from_list(manuals, "manual")

    return chosen_prompt, chosen_manual
