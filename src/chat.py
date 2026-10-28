from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# API Authentication
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = {"role": "system", "content": "You are a helpful AI assistant"}

conversation_history = []

def chat(user_input, history):
    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[SYSTEM_PROMPT] + history
    )
    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})
    return assistant_message, history

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break

        response, conversation_history = chat(user_input, conversation_history)

        print("Chatbot: ", response)