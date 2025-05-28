# DoPES
**D**ifferent Types **o**f **P**rompts (zero-shot, few-shot and prompt chaining) for **E**valuating Text-Based **S**olutions.

A collection of reusable, well-documented prompts for ChatGPT, designed to evaluate text-based solutions. Depending on the language and the prompt design, a distinction is made between German and English as well as zero-shot, few-shot and prompt chaining.

## Prompts
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

## Structure
```text
chatgpt-prompts/
├── README.md
├── prompts/
│   ├── en/
│   │   ├── zero-shot/
│   │   │   ├── 01_test.md
│   │   │   ├── 02_test.md
│   │   ├── few-shot/
│   │   │   ├── 01_test.md
│   │   │   ├── 02_test.md
│   │   ├── prompt-chaining/
│   │       ├── 01_test.md
│   │       ├── 02_test.md
│   ├── de/
│   │   ├── zero-shot/
│   │   │   ├── 01_test.md
│   │   │   ├── 02_test.md
│   │   ├── few-shot/
│   │   │   ├── 01_test.md
│   │   │   ├── 02_test.md
│   │   ├── prompt-chaining/
│   │       ├── 01_test.md
│   │       ├── 02_test.md
└── tags.json
```

### tags.json 
... is an metadata file that helps describe and organize the prompts programmatically.

## How to Use
1. Open a file in the `prompts/[language]` folder.
2. Customize the variables inside the prompt.
3. Paste it into ChatGPT or use via the OpenAI API.
