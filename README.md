# AI-chatbot

A terminal-based AI chatbot built in Python, designed to grow into a fully featured multi-provider LLM platform. Starting with the OpenAI API, this project is being developed incrementally — each phase adding meaningful capability while keeping the codebase clean and understandable.

## Current Features

- Conversational interface via the terminal
- OpenAI GPT model integration
- Secure API key management via `.env`
- Stateful conversation history: the model remembers the whole conversation
- Persistent conversations: saved automatically after every reply and resumable later
- Crash-safe saving using atomic writes, so a conversation file is never left half-written
- Startup menu listing conversations by title, last modified date and message count
- Custom conversation titles, or an automatically generated title if left blank
- Recap of the most recent exchanges when resuming a conversation
- Graceful handling of API errors and Ctrl+C

## Roadmap

The following features are planned and will be added progressively:

- [x] Stateful conversation history within a session
- [x] Persistent conversation history (save/load sessions)
- [ ] In-chat commands: `/history`, `/rename`, `/model`, `/help`
- [ ] Mid-conversation model switching, with each reply labelled by model
- [ ] Support for additional LLM providers (Groq, Ollama)
- [ ] Pre-flight token and cost estimation

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

- **Windows:** `python -m venv .venv`
- **macOS/Linux:** `python3 -m venv .venv`

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

### 6. Using the chatbot

On startup, choose a saved conversation by number or press `N` to start a new one.
New conversations ask for a title (leave it blank to have one generated after the first reply).

Type your message and press Enter to chat.

Conversations save automatically after every reply. Type `quit`, `exit` or `bye`
to leave, or press Ctrl+C. Nothing is lost upon exit.

Conversations are stored locally in the `conversations/` folder. Messages are sent to the model provider (currently OpenAI) to generate replies.

## Project Structure

```
AI-chatbot/
├── .env                      # API keys (never committed)
├── .gitignore
├── requirements.txt
├── README.md
├── LICENSE
├── conversations/            # saved conversations (created automatically)
└── src/
    ├── chat.py               # terminal interface and chat loop
    └── storage.py            # saving, loading, and listing conversations
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
