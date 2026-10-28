# AI-chatbot

A terminal-based AI chatbot built in Python, designed to grow into a fully featured multi-provider LLM platform. Starting with the OpenAI API, this project is being developed incrementally — each phase adding meaningful capability while keeping the codebase clean and understandable.

## Current Features

- Conversational interface via the terminal
- OpenAI GPT model integration
- Secure API key management via `.env`

## Roadmap

The following features are planned and will be added progressively:

- [x] Stateful conversation history within a session
- [ ] Persistent conversation history (save/load sessions)
- [ ] Support for additional LLM providers
- [ ] Mid-conversation model switching

## Tech Stack

- **Python 3.12+**
- **OpenAI Python SDK**
- **python-dotenv**

## Prerequisites

Ensure you have the following installed:

- [Python 3.12+](https://www.python.org/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/Download) _(recommended)_
- An [OpenAI API key](https://platform.openai.com/api-keys) with available credits

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ShridharSingh/AI-chatbot.git
cd AI-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- **Windows:** `.venv\Scripts\activate`
- **macOS/Linux:** `source .venv/bin/activate`

  > A virtual environment isolates your project dependencies and prevents version conflicts with other Python projects on your system.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the root of the project:

```
OPENAI_API_KEY="sk-xxx"
```

> Never commit your `.env` file. It is already excluded via `.gitignore`.

### 5. Run the chatbot

```bash
python src/chat.py
```

Type your message and press Enter to chat. Type `quit`, `exit`, or `bye` to end the session.

## Project Structure

```
AI-chatbot/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── LICENSE
└── src/
    └── chat.py
```

> The `src/` directory will expand as new providers, memory modules, and integrations are added.

## Pricing

OpenAI charges per token used. Check current model pricing before running extended sessions:
[https://openai.com/pricing](https://openai.com/pricing)

## License

Copyright (c) 2025 Shridhar Singh. All rights reserved.

This project is proprietary software. No part of this codebase may be
copied, modified, distributed, or used without explicit written
permission from the author.
