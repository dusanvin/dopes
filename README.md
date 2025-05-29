# DoPES
**D**ifferent Types **o**f **P**rompts (Zero-shot Learning, Few-shot Learning and Chain-of-Thought prompting) for **E**valuating Text-Based **S**olutions.

## Deutsch
Eine Sammlung von wiederverwendbaren, gut dokumentierten Prompts für ChatGPT, um textbasierte Lösungen zu evaluieren. Je nach Sprache und Prompt-Design wird zwischen Deutsch und Englisch sowie 
- Lernen ohne Beispiele (engl., Zero-shot learning, ZSL)
- Lernen mit wenigen Beispielen (engl., Few-shot Learning, FSL)
- ZSL mit strukturiertem Denken (engl., Chain-of-Thougt, CoT) und
- FSL with CoT
unterschieden.

### Projektstruktur
<details>
  <summary>Aufklappen zum Ansehen</summary>
```text
dopes/
├── README.md
├── .env.example
├── run_prompts.py
├── data/
│   ├── data.xlsx
├── manuals/
│   ├── zero-shot.pdf
│   ├── few-shot.pdf
│   ├── chain-of-thought.pdf
├── prompts/
│   ├── en/
│   │   ├── zero-shot/
│   │   │   ├── 01_test.md
│   │   │   ├── 02_test.md
│   │   ├── few-shot/
│   │   │   ├── 01_test.md
│   │   │   ├── 02_test.md
│   │   ├── chain-of-thought/
│   │       ├── 01_test.md
│   │       ├── 02_test.md
│   ├── de/
│   │   ├── zero-shot/
│   │   │   ├── (1)zsl+du.md
│   │   │   ├── 02_test.md
│   │   ├── few-shot/
│   │   │   ├── 01_test.md
│   │   │   ├── 02_test.md
│   │   ├── chain-of-thought/
│   │       ├── 01_test.md
│   │       ├── 02_test.md
├── responses/
│   ├── zero-shot/
│   │   ├── 1.md
│   │   ├── 2.md
│   ├── few-shot/
│   │   ├── 1.md
│   │   ├── 2.md
│   ├── chain-of-thought/
│   │   ├── 1.md
│   │   ├── 2.md
└── tags.json
```
</details>

## English
A collection of reusable, well-documented prompts for ChatGPT, designed to evaluate text-based solutions. Depending on the language and the prompt design, a distinction is made between German and English as well as 
- Zero-shot learning (ZSL)
- Few-shot Learning (FSL)
- ZSL with Chain-of-Thougt(CoT) prompting and
- FSL with CoT prompting

### Structure
```text
dopes/
├── README.md
├── .env.example
├── run_prompts.py
├── data/
│   ├── data.xlsx
├── manuals/
│   ├── zero-shot.pdf
│   ├── few-shot.pdf
│   ├── chain-of-thought.pdf
├── prompts/
│   ├── en/
│   │   ├── zero-shot/
│   │   │   ├── 01_test.md
│   │   │   ├── 02_test.md
│   │   ├── few-shot/
│   │   │   ├── 01_test.md
│   │   │   ├── 02_test.md
│   │   ├── chain-of-thought/
│   │       ├── 01_test.md
│   │       ├── 02_test.md
│   ├── de/
│   │   ├── zero-shot/
│   │   │   ├── (1)zsl+du.md
│   │   │   ├── 02_test.md
│   │   ├── few-shot/
│   │   │   ├── 01_test.md
│   │   │   ├── 02_test.md
│   │   ├── chain-of-thought/
│   │       ├── 01_test.md
│   │       ├── 02_test.md
├── responses/
│   ├── zero-shot/
│   │   ├── 1.md
│   │   ├── 2.md
│   ├── few-shot/
│   │   ├── 1.md
│   │   ├── 2.md
│   ├── chain-of-thought/
│   │   ├── 1.md
│   │   ├── 2.md
└── tags.json
```

### Prompts
Each prompt is located in a standalone Markdown file (*.md) in a subfolder of `prompts/[language]` and includes:
- Purpose
- Prompt template
- Instructions
- Example output

Prompts were structured using the following guidelines:
- https://github.com/dair-ai/Prompt-Engineering-Guide
- https://platform.openai.com/docs/guides/text?api-mode=responses#few-shot-learning
- https://cookbook.openai.com/examples/gpt4-1_prompting_guide
- https://www.reddit.com/r/ChatGPTPro/comments/1jzyf6k/openai_just_dropped_a_detailed_prompting_guide/

### .env.example
... is the example .env which should containt your API-key for ChatGPT.

### run_prompts.py
... is the file which loads your prompts as well as your grid, sends them via the API to ChatGPT and saves the generated response to your system.

### (1)zsl+du.md
... is a zero-shot prompt for evaluating text-based solutions.

### data/data.xlsx
... is the file which contains the text-based solutions to be evaluated.

### tags.json 
... is an metadata file that helps describe and organize the prompts programmatically.

## How to Use
1. Change the API-Key in the .env.example. Rename the file to .env
2. Convert your grid for evaluating qualitative data (depending on your shot) to "manual.pdf" (Base64-encoded form). Place it under manuals/
3. Customize your prompt in prompts/(1)zsl+du.md
4. Move to your project folder. Run the program via: ```python run_prompts.py```
