from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# API Authentication
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat(prompt):
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break

        response = chat(user_input)

        print("Chatbot: ", response)