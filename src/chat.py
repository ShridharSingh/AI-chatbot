"""Terminal interface: conversation menu, chat loop and title generation."""
from openai import OpenAI, APIError
from dotenv import load_dotenv
from datetime import datetime
import os

from storage import new_conversation, save_conversation, list_conversations

load_dotenv()

# API Authentication
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-5.4-mini"
SYSTEM_PROMPT = {"role": "system", "content": "You are a helpful AI assistant"}
RECAP_EXCHANGES = 3

def format_date(iso_string):
    """Converts the stored ISO date into readable format for startup menu."""
    return datetime.fromisoformat(iso_string).strftime("%d %b %Y, %H:%M")

def start_new_conversation():
    """Asks for a title, then creates an empty conversation."""
    title = input("Title (leave blank to generate one automatically): ").strip()
    return new_conversation(title)

def choose_conversation():
    """Displays conversation list to user, allowing user to either continue a previous 
    conversation or start a new one. Starts a new conversation if none exist."""
    conversations = list_conversations()

    # If no previous conversations, start new conversation.
    if not conversations:
        print("No saved conversations yet. Starting a new one.")
        return start_new_conversation()

    # Shows numbered list of previous conversations, sorted by last modified.
    print("Your conversations:")
    for i, conv in enumerate(conversations, start=1):
        title = conv["title"] or "Untitled"
        date = format_date(conv["last_modified"])
        count = len(conv["messages"])
        print(f" {i}. {title:<30} {date}    ({count} messages)")

    while True:
        choice = input("\nEnter a number to continue a conversation, or N for a new one: ").strip()
        if choice.lower() == "n":
            return start_new_conversation()
        # Checks if input is valid number and matches a listed conversation.
        if choice.isdigit() and 1 <= int(choice) <= len(conversations):  
            return conversations[int(choice) -1]
        print(f"Please enter a number from 1 to {len(conversations)}, or N.")

def show_recap(messages):
    """Checks if previous messages exist in conversation and displays the most recent exchanges."""
    if not messages:
        return
    recent = messages[-RECAP_EXCHANGES * 2:]
    print(f"({len(messages)} messages. Showing the last {len(recent) // 2} exchanges.)\n")
    for message in recent:
        speaker = "You" if message["role"] == "user" else "Chatbot"
        print(f" {speaker}: {message['content']}\n")

def chat(user_input, messages):
    """Sends system prompt, history and new message to the model and adds both user and chatbot messages only after a successful reply."""
    request = [SYSTEM_PROMPT] + messages + [{"role": "user", "content": user_input}]
    response = client.chat.completions.create(model=MODEL, messages=request)
    reply = response.choices[0].message.content

    # Only added to history once the API call has succeeded
    messages.append({"role": "user", "content": user_input})
    messages.append({"role": "assistant", "content": reply})
    return reply

def generate_title(messages):
    """LLM generates title based on first exchange in conversation. """
    instruction = {
        "role": "user",
        "content": "Write a short title (at most 6 words) for this conversation. "
        "Reply with title only, no quotation marks"
    }
    try:
        response = client.chat.completions.create(model=MODEL, messages=messages[:2] + [instruction])
        return response.choices[0].message.content.strip().strip('"')
    except APIError:
        return "Untitled" # a failed title should never stop the chat


if __name__ == "__main__":
    conversation = choose_conversation()
    print(f"\n--- {conversation['title'] or 'New conversation'} ---")
    show_recap(conversation["messages"])

    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Goodbye!")
                break

            try:
                reply = chat(user_input, conversation["messages"])
            except APIError as error:
                print(f"Couldn't get a reply ({error}). Your message wasn't saved. Please try again. \n")
                continue

            print(f"Chatbot: {reply}\n")

            if not conversation["title"]:
                conversation["title"] = generate_title(conversation["messages"])
                print(f"(Conversation titled: {conversation['title']})\n")

            save_conversation(conversation) # Auto-saves the conversation after every reply so nothing is lost.

    except KeyboardInterrupt:
        # Accepts Ctrl + C and exits. Conversation auto-saves after the last reply.
        print("\nGoodbye! Your conversation is saved.")