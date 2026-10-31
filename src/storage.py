"""Saves, loads and lists conversations as JSON files."""
import json
import os
import tempfile
import uuid
from datetime import datetime 
from pathlib import Path

CONVERSATION_DIR = Path(__file__).resolve().parent.parent / "conversations"

def _now():
    """Returns current system time in ISO format."""
    # Stored as ISO text. Avoids writing date object to json, 
    # readable, and sorts correctly as text and converts back with fromisoformat().
    return datetime.now().isoformat(timespec="seconds")

def new_conversation(title=""):
    """Creates a new, empty conversation with a unique ID, title, creation
    date and last modified date. Title is optional."""
    now = _now()
    return {
        # Unique ID, also used as file name. Comprises creation date, then the first
        # 8 hex characters of a random 128-bit UUID. Date prefix keeps files in order 
        # of creation.
        "id": f"{datetime.now():%Y-%m-%d}_{uuid.uuid4().hex[:8]}", 
        "title": title,
        "created": now,
        "last_modified": now,
        "messages": [],
    }

def save_conversation(conversation):
    """Creates conversation directory if one doesn't exist. Performs an atomic write
    from mkstemp temp file to JSON file. Conversation is saved using unique name and
    updates last_modified."""
    CONVERSATION_DIR.mkdir(exist_ok=True)
    conversation["last_modified"] = _now()
    path = CONVERSATION_DIR / f"{conversation['id']}.json"

    # Atomic write: save to a temp file, then swap it into place in one step,
    # so a crash mid-save can never leave a half-written conversation.
    # mkstemp creates the temp file safely and doesn't auto-delete it.
    # It must be in the same folder so os.replace stays on the same drive.
    fd, temp_path = tempfile.mkstemp(dir=CONVERSATION_DIR, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(conversation, f, indent=2, ensure_ascii=False)
    os.replace(temp_path, path)

def load_conversation(path):
    """Opens a conversation saved as JSON file back into a dictionary."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def list_conversations():
    """Creates conversation directory if it doesn't exist. Returns list of stored 
    conversations in order of newest first. Conversations are only recognised 
    when stored in .json format."""
    CONVERSATION_DIR.mkdir(exist_ok=True)
    conversations = []
    for path in CONVERSATION_DIR.glob("*.json"):
        try:
            conversations.append(load_conversation(path))
        except (json.JSONDecodeError, OSError):
            continue # skips a damaged file instead of crashing
    return sorted(conversations, key=lambda c: c["last_modified"], reverse=True)