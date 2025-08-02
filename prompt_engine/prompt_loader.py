from pathlib import Path

def load_prompt_and_raster(prompt_path: Path, raster_path: Path):
    with open(prompt_path, "r", encoding="utf-8") as f:
        raw_prompt = f.read()
    with open(raster_path, "r", encoding="utf-8") as f:
        raster_text = f.read()
    return raw_prompt, raster_text
